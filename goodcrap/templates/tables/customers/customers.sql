CREATE TABLE if not exists customers (
  customer_number varchar(11) NOT NULL,
  first_name varchar(50) NOT NULL,
  last_name varchar(50) NOT NULL,
  phone varchar(50) NOT NULL,
  address_line varchar(50) NOT NULL,
  city varchar(50) NOT NULL,
  state varchar(50) DEFAULT NULL,
  postalcode varchar(15) DEFAULT NULL,
  country varchar(50) NOT NULL,
  date_of_birth date,
  credit_limit real,
  income real,
  PRIMARY KEY (customer_number)
);
