#include <cxxopts.hpp>
#include "constants.h"

int main(int argc, char **argv) {
    cxxopts::Options options("steerBasicDirs", "Determine basic incident directions");
    options.add_options()
        ("h,hex", "Hexagon file name", cxxopts::value<std::string>())
        ("z,zvals", "Z-values file name", cxxopts::value<std::string>())
        ("help", "Print help");

    auto result = options.parse(argc, argv);

    if (result.count("help")) {
        cout << options.help() << endl;
        return 0;
    }

    if (!result.count("hex") || !result.count("zvals")) {
        cout << "Error: missing required arguments" << endl;
        cout << options.help() << endl;
        return 1;
    }

    string hname = result["hex"].as<std::string>();
    string zname = result["zvals"].as<std::string>();
    MatrixXd wi = readData("data/" + zname + "/wi.txt");
    MatrixXd hexagons = readData("include/hexagons/" + hname + ".txt");
    
    // Determine the set of incident directions to use for simulations
    int num_query = wi.rows();
    int num_hexagon = hexagons.rows();
    MatrixXd query = MatrixXd::Zero(num_query, 3);
    query.block(0, 0, num_query, 2) = wi;
    vector<int> directions;
    for (int i = 0; i < num_query; i++) {
        double theta_i = wi(i, 0);
        double phi_i = wi(i, 1);
        double xc = sin(theta_i) * cos(phi_i);
        double yc = sin(theta_i) * sin(phi_i);
        int choice = 0;
        double min_dist = sqrt(pow(xc - hexagons(0, 0), 2) + pow(yc - hexagons(0, 1), 2));
        for (int j = 1; j < num_hexagon; j++) {
            double dist = sqrt(pow(xc - hexagons(j, 0), 2) + pow(yc - hexagons(j, 1), 2));
            if (dist < min_dist) {
                choice = j;
                min_dist = dist;
            }
        }
        directions.push_back(choice);
    }
    set<int> unique_dir(directions.begin(), directions.end());

    // Write files to specify basic incident directions to use in simulations
    int num_dir = unique_dir.size();
    MatrixXd basic(num_dir, 2);
    int count = 0;
    for (int d : unique_dir) {
        basic(count, 0) = hexagons(d, 2);
        basic(count, 1) = hexagons(d, 3);
        for (int i = 0; i < num_query; i++) {
            if (directions[i] == d)
                query(i, 2) = count * 1.0;
        }
        count += 1;
    }
    writeBinary("data/" + zname + "/basic.binary", basic);
    writeBinary("data/" + zname + "/query.binary", query);
    printf("Need to perform simulations using %d incident directions.\n", count);
}