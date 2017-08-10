#ifndef EXAMPLE_H
#define EXAMPLE_H

class example_class {
	private:
		double favorite;
		
	public:
		example_class(double favorite);
		~example_class();

		double getFavorite();
		double Add(double a, double b);
		double Multiply(double a, double b);
};


#ifdef __cplusplus
extern "C" {
#endif

//#ifdef EXAMPLE_EXPORT
//#define EXAMPLE_API __declspec(dllexport)
//#else
//#define EXAMPLE_API __declspec(dllimport)
//#endif

	example_class* new_example_class(double favorite);

	void del_example_class(example_class *example);

	double example_add(example_class* example, double a, double b);

#ifdef __cplusplus
}
#endif

#endif //EXAMPLE_H
