#include "example.h"

		double favorite;
		
		
example_class::example_class(double favorite) {
	this->favorite = favorite;
}
example_class::~example_class(){}

		
double example_class::getFavorite() { return this->favorite; }
double example_class::Add(double a, double b) { return this->favorite + a + b; }
double example_class::Multiply(double a, double b) {
	return this->favorite * a * b;
}


example_class* new_example_class(double favorite) {
	return new example_class(favorite);
}

void del_example_class(example_class *maths) {
	maths->~example_class();
}

double example_add(example_class* example, double a, double b) {
	return example->Add(a,b);
}
