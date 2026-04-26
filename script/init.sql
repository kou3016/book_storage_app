USE book_app;

CREATE TABLE book(
    id int(11) not null primary key auto_increment,
    title varchar(255) not null,
    author varchar(255) not null,
    volumes int(11) null,
    pulisher varchar(255) null,
    isbn varchar(255) null,
    genre varchar(255) null,
    status varchar(255) null,
    total_reading_time int(11) null,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp null default current_timestamp on update current_timestamp
);

CREATE TABLE reading_log(
    id int(11) not null primary key auto_increment,
    foreign key book_id (id) references book(id),
    memo varchar(255) null,
    reading_time int(11) null,
    reading_data timestamp not null default current_timestamp,
    created_at timestamp not null default current_timestamp
);

CREATE TABLE reviews(
    id int(11) not null primary key auto_increment,
    foreign key book_id (id) references book(id),
    contents varchar(255) null,
    rating int(11) null,
    created_at timestamp not null default current_timestamp,
    updated_at timestamp null default current_timestamp on update current_timestamp
);