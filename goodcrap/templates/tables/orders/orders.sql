CREATE TABLE if not exists orders (
  order_number varchar(11) NOT NULL,
  order_date date NOT NULL,
  shipping_date date DEFAULT NULL,
  order_status varchar(15) NOT NULL,
  product varchar(15) NOT NULL,
  quantity_ordered int NOT NULL,
  unit_price real NOT NULL,
  customer_number varchar(11) NOT NULL,
  PRIMARY KEY (order_number),
  CONSTRAINT fk_orders_customers FOREIGN KEY (customer_number) REFERENCES customers (customer_number)
);