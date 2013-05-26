struct Transheader {
    char supplier_no[10],
         customer_no[10],
         account_no[10],
         folio_year[4],
         folio_mo[2],
         folio_no[2];
         struct keys {
             char trans_ref_no[10];
         };
         char term_id[7],
         load_date[6],
         load_time[4],
         driver_no[10],
         truck_no[8];
};
