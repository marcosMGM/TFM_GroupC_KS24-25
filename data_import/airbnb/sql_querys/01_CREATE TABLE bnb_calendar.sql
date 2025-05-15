CREATE TABLE bnb_calendar (
    property_id BIGINT NOT NULL,
    date DATE NOT NULL,
    available BIT,
    price DECIMAL(10,2),
    minimum_nights INT,
    maximum_nights INT,
    PRIMARY KEY (property_id, date)
);


