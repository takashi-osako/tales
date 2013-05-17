#define SIZE 10

struct book {
	char title[SIZE];
	char description[12];
	
	struct ack {
	   char name[6];
	} names[2];
};