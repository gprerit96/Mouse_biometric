#include <opencv2\opencv.hpp>
#include <fstream>
#include <string>
#include <cstring>
#include <math.h>
#include <iomanip>
#include <windows.h>

using namespace std;
using namespace cv;


int main() {

	ifstream inputfile("C://Users/salimatte/Downloads/BTP/BTP_Codes/features/ProcessedFeatures.csv");
	string current_line;
	ofstream myfile;
	myfile.open("resultsf.txt");
	getline(inputfile, current_line);
	while (getline(inputfile, current_line)) {
		cout << current_line << endl;
		stringstream temp(current_line);
		string single_value;
		getline(temp, single_value, ',');
		Mat Hold_Time(1, 10, CV_64F);
		int y = 0;
		while (getline(temp, single_value, ',')) {
			// convert the string element to a integer value
			Hold_Time.at<double>(0, y) = atoi(single_value.c_str());
			y++;
		}
		Vec2d pred_res;
		EM user;
		string trained_model_loc = "mouse.yml";
		FileStorage fs(trained_model_loc, FileStorage::READ);
		fs.open(trained_model_loc, FileStorage::READ);
		//if the file is not opened then return 0.0
		if (!(fs.isOpened()))
		{
			return 1;
		}
		FileNode fn(fs.root(0));
		//opening the classifier
		user.read(fn);
		//testing the classifier with time
		pred_res = user.predict(Hold_Time);
		fs.release();
		char* result = new char[40];
		sprintf(result, "%d------%f\n", (pred_res(0)>=-500000)?0:1, pred_res(1));
		myfile << result;
	}
	myfile.close();
	return 0;
}