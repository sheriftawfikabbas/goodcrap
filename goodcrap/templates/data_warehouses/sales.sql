/*
This data warehouse is greatly inspired by the Oracle sample data warehouse:
https://docs.oracle.com/cd/A91034_01/DOC/server.901/a90237/appb.htm
*/

/*Dimension: times */

CREATE TABLE times (
    time_id DATE,
    day_name VARCHAR2(9) CONSTRAINT tim_day_name_nn NOT NULL,
    day_number_in_week NUMBER(1) CONSTRAINT tim_day_in_week_nn NOT NULL,
    day_number_in_month NUMBER(2) CONSTRAINT tim_day_in_month_nn NOT NULL,
    calendar_week_number NUMBER(2) CONSTRAINT tim_cal_week_nn NOT NULL,
    fiscal_week_number NUMBER(2) CONSTRAINT tim_fis_week_nn NOT NULL,
    week_ending_day DATE CONSTRAINT tim_week_ending_day_nn NOT NULL,
    calendar_month_number NUMBER(2) CONSTRAINT tim_cal_month_number_nn NOT NULL,
    fiscal_month_number NUMBER(2) CONSTRAINT tim_fis_month_number_nn NOT NULL,
    calendar_month_desc VARCHAR2(8) CONSTRAINT tim_cal_month_desc_nn NOT NULL,
    fiscal_month_desc VARCHAR2(8) CONSTRAINT tim_fis_month_desc_nn NOT NULL,
    days_in_cal_month NUMBER CONSTRAINT tim_days_cal_month_nn NOT NULL,
    days_in_fis_month NUMBER CONSTRAINT tim_days_fis_month_nn NOT NULL,
    end_of_cal_month DATE CONSTRAINT tim_end_of_cal_month_nn NOT NULL,
    end_of_fis_month DATE CONSTRAINT tim_end_of_fis_month_nn NOT NULL,
    calendar_month_name VARCHAR2(9) CONSTRAINT tim_cal_month_name_nn NOT NULL,
    fiscal_month_name VARCHAR2(9) CONSTRAINT tim_fis_month_name_nn NOT NULL,
    calendar_quarter_desc CHAR(7) CONSTRAINT tim_cal_quarter_desc_nn NOT NULL,
    fiscal_quarter_desc CHAR(7) CONSTRAINT tim_fis_quarter_desc_nn NOT NULL,
    days_in_cal_quarter NUMBER CONSTRAINT tim_days_cal_quarter_nn NOT NULL,
    days_in_fis_quarter NUMBER CONSTRAINT tim_days_fis_quarter_nn NOT NULL,
    end_of_cal_quarter DATE CONSTRAINT tim_end_of_cal_quarter_nn NOT NULL,
    end_of_fis_quarter DATE CONSTRAINT tim_end_of_fis_quarter_nn NOT NULL,
    calendar_quarter_number NUMBER(1) CONSTRAINT tim_cal_quarter_number_nn NOT NULL,
    fiscal_quarter_number NUMBER(1) CONSTRAINT tim_fis_quarter_number_nn NOT NULL,
    calendar_year NUMBER(4) CONSTRAINT tim_cal_year_nn NOT NULL,
    fiscal_year NUMBER(4) CONSTRAINT tim_fis_year_nn NOT NULL,
    days_in_cal_year NUMBER CONSTRAINT tim_days_cal_year_nn NOT NULL,
    days_in_fis_year NUMBER CONSTRAINT tim_days_fis_year_nn NOT NULL,
    end_of_cal_year DATE CONSTRAINT tim_end_of_cal_year_nn NOT NULL,
    end_of_fis_year DATE CONSTRAINT tim_end_of_fis_year_nn NOT NULL,
    PRIMARY KEY (time_id)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Dimension: channels */
CREATE TABLE channels (
    channel_id CHAR(1),
    channel_desc VARCHAR2(20) CONSTRAINT chan_desc_nn NOT NULL,
    channel_class VARCHAR2(20),
    PRIMARY KEY (channel_id)
);

/*Dimension: promotions */
CREATE TABLE promotions (
    promo_id NUMBER(6),
    promo_name VARCHAR2(20) CONSTRAINT promo_name_nn NOT NULL,
    promo_subcategory VARCHAR2(30) CONSTRAINT promo_subcat_nn NOT NULL,
    promo_category VARCHAR2(30) CONSTRAINT promo_cat_nn NOT NULL,
    promo_cost NUMBER(10, 2) CONSTRAINT promo_cost_nn NOT NULL,
    promo_begin_date DATE CONSTRAINT promo_begin_date_nn NOT NULL,
    promo_end_date DATE CONSTRAINT promo_end_date_nn NOT NULL,
    PRIMARY KEY (promo_id)
);

/*Dimension: countries */
CREATE TABLE countries (
    country_id CHAR(2),
    country_name VARCHAR2(40) CONSTRAINT country_country_name_nn NOT NULL,
    country_subregion VARCHAR2(30),
    country_region VARCHAR2(20)
);

/*Dimension: customers */
CREATE TABLE customers (
    cust_id NUMBER,
    cust_first_name VARCHAR2(20) NOT NULL,
    cust_last_name VARCHAR2(40) NOT NULL,
    cust_gender CHAR(1),
    cust_year_of_birth NUMBER(4),
    cust_marital_status VARCHAR2(20),
    cust_street_address VARCHAR2(40) NOT NULL,
    cust_postal_code VARCHAR2(10) NOT NULL,
    cust_city VARCHAR2(30) NOT NULL,
    cust_state_province VARCHAR2(40),
    country_id CHAR(2) NOT NULL,
    cust_main_phone_number VARCHAR2(25),
    cust_income_level VARCHAR2(30),
    cust_credit_limit NUMBER,
    cust_email VARCHAR2(30)
);

/*Dimension: products */
CREATE TABLE products (
    prod_id NUMBER(6),
    prod_name VARCHAR2(50) CONSTRAINT products_prod_name_nn NOT NULL,
    prod_desc VARCHAR2(4000) CONSTRAINT products_prod_desc_nn NOT NULL,
    prod_subcategory VARCHAR2(50) CONSTRAINT products_prod_subcat_nn NOT NULL,
    prod_subcat_desc VARCHAR2(2000) CONSTRAINT products_prod_subcatd_nn NOT NULL,
    prod_category VARCHAR2(50) CONSTRAINT products_prod_cat_nn NOT NULL,
    prod_cat_desc VARCHAR2(2000) CONSTRAINT products_prod_catd_nn NOT NULL,
    prod_weight_class NUMBER(2),
    prod_unit_of_measure VARCHAR2(20),
    prod_pack_size VARCHAR2(30),
    supplier_id NUMBER(6),
    prod_status VARCHAR2(20) CONSTRAINT products_prod_stat_nn NOT NULL,
    prod_list_price NUMBER(8, 2) CONSTRAINT products_prod_list_price_nn NOT NULL,
    prod_min_price NUMBER(8, 2) CONSTRAINT products_prod_min_price_nn NOT NULL
);

/*Dimension: sales */
CREATE TABLE sales (
    prod_id NUMBER(6) CONSTRAINT sales_product_nn NOT NULL,
    cust_id NUMBER CONSTRAINT sales_customer_nn NOT NULL,
    time_id DATE CONSTRAINT sales_time_nn NOT NULL,
    channel_id CHAR(1) CONSTRAINT sales_channel_nn NOT NULL,
    promo_id NUMBER(6),
    quantity_sold NUMBER(3) CONSTRAINT sales_quantity_nn NOT NULL,
    amount NUMBER(10, 2) CONSTRAINT sales_amount_nn NOT NULL,
    cost NUMBER(10, 2) CONSTRAINT sales_cost_nn NOT NULL
);

ALTER TABLE
    sales
ADD
    (
        CONSTRAINT sales_product_fk FOREIGN KEY (prod_id) REFERENCES products,
        CONSTRAINT sales_customer_fk FOREIGN KEY (cust_id) REFERENCES customers,
        CONSTRAINT sales_time_fk FOREIGN KEY (time_id) REFERENCES times,
        CONSTRAINT sales_channel_fk FOREIGN KEY (channel_id) REFERENCES channels
    );
