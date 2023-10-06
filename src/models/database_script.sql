create schema if not exists parkingmanagement;

create table if not exists parkingmanagement.employee
(
    id int not null auto_increment, 
    emp_name varchar(20) not null, 
    email varchar(50) not null, 
    phone_number varchar(12), 
    primary key (id)
);

create table if not exists parkingmanagement.credentials
(
    id int not null auto_increment, 
    username varchar(20) not null, 
    password varchar(50) not null, 
    user_id int, 
    foreign key (user_id) references employee(id),
    primary key (id)
);

create table if not exists parkingmanagement.roles
(
    id int not null auto_increment, 
    role_category varchar(20) not null, 
    primary key (id)
);

create table if not exists parkingmanagement.role_mapping
(
    id int not null auto_increment, 
    user_id int not null, 
    role_id int not null, 
    foreign key (user_id) references employee(id),
    foreign key (role_id) references roles(id),    
    primary key (id)
);

create table if not exists parkingmanagement.slot_category
(
    id int not null auto_increment, 
    slot_type varchar(10) not null, 
    total_capacity int not null, 
    charge int not null,
    primary key (id)
);

create table if not exists parkingmanagement.slot_status
(
    id int not null auto_increment, 
    category varchar(20) not null,
    primary key (id)
);
insert into parkingmanagement.slot_status(category) values('Not Allowed');
insert into parkingmanagement.slot_status(category) values('Allowed');

create table if not exists parkingmanagement.customer
(
    id int not null auto_increment, 
    customer_name int not null, 
    email int not null, 
    phone_number int not null,
    primary key (id)
);

create table if not exists parkingmanagement.vehicle
(
    id int not null auto_increment, 
    customer_id int not null,
    vehicle_number varchar(20) not null, 
    slot_category_id int not null,
    foreign key (customer_id) references customer(id), 
    foreign key (slot_category_id) references slot_category(id), 
    primary key (id)
);


create table if not exists parkingmanagement.slot
(
    id int not null auto_increment, 
    slot_number int not null, 
    vehicle_id int not null, 
    slot_category_id int not null,
    status_id int not null,
    billing_id int not null,
    foreign key (vehicle_id) references vehicle(id),
    foreign key (slot_category_id) references slot_category(id), 
    foreign key (status_id) references slot_status(id), 
    foreign key (billing_id) references billing(id),
    primary key (id)
);



create table if not exists parkingmanagement.billing
(
    id int not null auto_increment, 
    vehicle_id int not null, 
    bill_date date not null,
    time_parked_in time not null,
    time_parked_out time,
    total_charges int,
    foreign key (vehicle_id) references vehicle(id),
    primary key (id)
);