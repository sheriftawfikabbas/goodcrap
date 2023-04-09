/*
 This data warehouse is greatly inspired by the Oracle sample data warehouse:
 https://docs.oracle.com/cd/A91034_01/DOC/server.901/a90237/appb.htm
 */
/*Dimension: times */
CREATE TABLE times (
    time_id date,
    day_name varchar(9) NOT NULL,
    day_number_in_week int(1) NOT NULL,
    day_number_in_month int(2) NOT NULL,
    calendar_week_number int(2) NOT NULL,
    week_ending_day date NOT NULL,
    calendar_month_number int(2) NOT NULL,
    days_in_cal_month int NOT NULL,
    end_of_cal_month date NOT NULL,
    calendar_month_name varchar(9) NOT NULL,
    days_in_cal_quarter int NOT NULL,
    end_of_cal_quarter date NOT NULL,
    calendar_quarter_number int(1) NOT NULL,
    calendar_year int(4) NOT NULL,
    days_in_cal_year int NOT NULL,
    end_of_cal_year date NOT NULL,
    PRIMARY KEY (time_id)
) ENGINE = InnoDB DEFAULT CHARSET = latin1;

/*Dimension: channels */
CREATE TABLE channels (
    channel_id int,
    channel_desc varchar(20) NOT NULL,
    channel_class varchar(20),
    PRIMARY KEY (channel_id)
);

/*Dimension: promotions */
CREATE TABLE promotions (
    promo_id int(11),
    promo_name varchar(20) NOT NULL,
    promo_subcategory varchar(30) NOT NULL,
    promo_category varchar(30) NOT NULL,
    promo_cost decimal(10, 2) NOT NULL,
    promo_begin_date DATE NOT NULL,
    promo_end_date DATE NOT NULL,
    PRIMARY KEY (promo_id)
);

/*Dimension: countries */
CREATE TABLE countries (
    country_id CHAR(2),
    country_name varchar(40) NOT NULL,
    country_subregion varchar(30),
    country_region varchar(20),
    country_continent varchar(20)
);

/*Dimension: customers */
CREATE TABLE customers (
    cust_id int(11),
    cust_first_name varchar(20) NOT NULL,
    cust_last_name varchar(40) NOT NULL,
    cust_gender CHAR(1),
    cust_year_of_birth int(4),
    cust_marital_status varchar(20),
    cust_street_address varchar(40) NOT NULL,
    cust_postal_code varchar(10) NOT NULL,
    cust_city varchar(30) NOT NULL,
    cust_state_province varchar(40),
    country_id CHAR(2) NOT NULL,
    cust_phone_number varchar(25),
    cust_income varchar(30),
    cust_credit_limit real,
    cust_email varchar(30)
);

/*Dimension: products */
CREATE TABLE products (
    prod_id int(11),
    prod_name varchar(50) NOT NULL,
    prod_desc text NOT NULL,
    prod_subcategory text NOT NULL,
    prod_subcat_desc varchar(2000) NOT NULL,
    prod_category varchar(50) NOT NULL,
    prod_cat_desc varchar(2000) NOT NULL,
    prod_weight_class int,
    prod_unit_of_measure varchar(20),
    prod_pack_size varchar(30),
    supplier_id int(6),
    prod_status varchar(20) NOT NULL,
    prod_list_price decimal(8, 2) NOT NULL,
    prod_min_price decimal(8, 2) NOT NULL
);

/*Dimension: sales */
CREATE TABLE sales (
    prod_id int(11) NOT NULL,
    cust_id int(11) NOT NULL,
    time_id date NOT NULL,
    channel_id int NOT NULL,
    promo_id int(11),
    quantity_sold int(11) NOT NULL,
    amount decimal(10, 2) NOT NULL,
    cost decimal(10, 2) NOT NULL
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