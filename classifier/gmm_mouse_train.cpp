#include <opencv2\opencv.hpp>
#include <fstream>
#include <string>
#include <math.h>
#include <iomanip>
#include <windows.h>

using namespace std;
using namespace cv;


int main() {
	ifstream inputfile("c://users/salimatte/downloads/btp/btp_codes/features/processedfeatures.csv");
	string current_line;
	// vector allows you to add data without knowing the exact size beforehand
	vector< vector<double> > all_data;
	// start reading lines as long as there are lines in the file
	getline(inputfile, current_line);
	while (getline(inputfile, current_line)) {
		// now inside each line we need to seperate the cols
		cout << current_line << endl;
		vector<double> values;
		stringstream temp(current_line);
		string single_value;
		getline(temp, single_value, ',');
		if (single_value == "1")break;

		while (getline(temp, single_value, ',')) {
			// convert the string element to a integer value
			values.push_back(atof(single_value.c_str()));
		}
		// add the row to the complete data vector
		all_data.push_back(values);
	}

	// now add all the data into a mat element
	cout << all_data.size() << "      " << all_data[0].size() << endl;
	mat vect = mat::zeros((int)all_data.size(), (int)all_data[0].size(), cv_64f);
	// loop over vectors and add the data
	for (int rows = 0; rows < (int)all_data.size(); rows++) {
		for (int cols = 0; cols< (int)all_data[0].size(); cols++) {
			vect.at<double>(rows, cols) = all_data[rows][cols];
		}
	}

	struct cvtermcriteria criteria;

	criteria.type = cv_termcrit_iter + cv_termcrit_eps;
	criteria.max_iter = 200;
	criteria.epsilon = 0.0000001;
	em user(2, em::cov_mat_diagonal, criteria);
	//fn to train the classifier
	user.train(vect);
	filestorage fs("mouse.yml", filestorage::write);

	string model_name = "vinay";
	//if classifier is trained then save it 
	if ((user.istrained()))
	{
		cout << "model trained for" << model_name << endl;
		user.write(fs);
		cout << "model for " << model_name << "is saved" << endl << endl;
		fs.release();
	}
	//if classifier is not trained then give error message
	else
	{
		cout << "model not trained for" << model_name << endl;
	}
	return 0;
}