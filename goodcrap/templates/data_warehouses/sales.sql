/*
 This snowflake-type data warehouse is greatly inspired by the oracle sample data warehouse:
 https://docs.oracle.com/cd/a91034_01/doc/server.901/a90237/appb.htm
 */
/*Dimension: times */
create table times (
    time_id date not null,
    day_name varchar(9) not null,
    day_number_in_week int not null,
    day_number_in_month int not null,
    calendar_week_number int not null,
    week_ending_day date not null,
    calendar_month_number int not null,
    days_in_cal_month int not null,
    end_of_cal_month date not null,
    calendar_month_name varchar(9) not null,
    days_in_cal_quarter int not null,
    end_of_cal_quarter date not null,
    calendar_quarter_number int not null,
    calendar_year int not null,
    days_in_cal_year int not null,
    end_of_cal_year date not null,
    primary key (time_id)
);

/*Dimension: channels */
create table channels (
    channel_id int not null,
    channel_desc varchar(20) not null,
    channel_class varchar(20),
    primary key (channel_id)
);

/*Dimension: promotions */
create table promotions (
    promo_id int not null,
    promo_name varchar(20) not null,
    promo_subcategory varchar(30) not null,
    promo_category varchar(30) not null,
    promo_cost real not null,
    promo_begin_date date not null,
    promo_end_date date not null,
    primary key (promo_id)
);

/*Dimension: countries */
create table countries (
    country_id char(2),
    country_name varchar(40) not null,
    country_subregion varchar(30),
    country_region varchar(20),
    country_continent varchar(20),
    primary key (country_id)
);

/*Dimension: customers */
create table customers (
    cust_id int,
    cust_first_name varchar(20) not null,
    cust_last_name varchar(40) not null,
    cust_gender char(1),
    cust_year_of_birth int,
    cust_marital_status varchar(20),
    cust_street_address varchar(40) not null,
    cust_postal_code varchar(10) not null,
    cust_city varchar(30) not null,
    cust_state_province varchar(40),
    country_id char(2) not null,
    cust_phone_number varchar(25),
    cust_income real,
    cust_credit_limit real,
    cust_email varchar(30),
    primary key (cust_id),
    constraint fk_customers_countries foreign key (country_id) references countries (country_id)
);

/*Dimension: products */
create table products (
    prod_id int,
    prod_name varchar(50) not null,
    prod_desc text not null,
    prod_subcategory text not null,
    prod_subcat_desc text not null,
    prod_category varchar(50) not null,
    prod_cat_desc text not null,
    prod_weight_class int,
    prod_unit_of_measure varchar(20),
    prod_pack_size varchar(30),
    supplier_id int,
    prod_status varchar(20) not null,
    prod_list_price real not null,
    prod_min_price real not null,
    primary key (prod_id)
);

/*Fact: sales */
create table sales (
    sale_id int not null,
    prod_id int not null,
    cust_id int not null,
    time_id date not null,
    channel_id int not null,
    promo_id int,
    quantity_sold int not null,
    amount real not null,
    cost real not null,
    primary key (sale_id),
    constraint fk_sales_product foreign key (prod_id) references products (prod_id),
    constraint fk_sales_customer foreign key (cust_id) references customers (cust_id),
    constraint fk_sales_time foreign key (time_id) references times (time_id),
    constraint fk_sales_channel foreign key (channel_id) references channels (channel_id)
);