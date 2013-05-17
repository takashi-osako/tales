#include "test2.h"
#define   NAME      10
 
struct address {
    char address_line1[SIZE];
    char country[2];
    char city[15];
    struct phone {
        char home[10];
        char mobile[10];
    }
    contact[2];
    
    struct person {
        char first_name[NAME];
        char last_name[NAME];
    }
    main_contact;
    char zip[5];
    
};
   
    