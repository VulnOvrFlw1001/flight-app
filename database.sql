CREATE TABLE states (
 id SERIAL PRIMARY KEY,
 state_code VARCHAR(2) NOT NULL,
 state_name VARCHAR(50) NOT NULL
);

CREATE TABLE flights (
  id SERIAL PRIMARY KEY,	
  departure_state VARCHAR(255) NOT NULL,
  arrival_state VARCHAR(255) NOT NULL,
  departure_time TIMESTAMP NOT NULL,
  arrival_time TIMESTAMP NOT NULL,
  price DECIMAL(10,2)
);

CREATE TABLE tickets(
  id SERIAL PRIMARY KEY,
  ticket_number VARCHAR(50) NOT NULL,
  departure VARCHAR(50) NOT NULL,
  arrival VARCHAR(50) NOT NULL,
  departure_time TIMESTAMP NOT NULL,
  arrival_time TIMESTAMP NOT NULL,
  ticket_price DECIMAL (10,2) NOT NULL,
  users VARCHAR(50) NOT NULL
);

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  email VARCHAR(50) NOT NULL
);

INSERT INTO states(state_code, state_name)
VALUES
('AL', 'Alabama'),
('AK', 'Alaska'),
('AZ', 'Arizona'),
('AR', 'Arkansas'),
('CA', 'California'),
('CO', 'Colorado'),
('CT', 'Connecticut'),
('DE', 'Delaware'),
('FL', 'Florida'),
('GA', 'Georgia'),
('HI', 'Hawaii'),
('ID', 'Idaho'),    
('IL', 'Illinois'),
('IN', 'Indiana'),
('IA', 'Iowa'),
('KS', 'Kansas'),
('KY', 'Kentucky'),
('LA', 'Louisiana'),
('ME', 'Maine'),
('MD', 'Maryland'),
('MA', 'Massachusetts'),
('MI', 'Michigan'),
('MN', 'Minnesota'),
('MS', 'Mississippi'),
('MO', 'Missouri'),
('MT', 'Montana'),
('NE', 'Nebraska'),
('NV', 'Nevada'),
('NH', 'New Hampshire'),
('NJ', 'New Jersey'),
('NM', 'New Mexico'),
('NY', 'New York'),
('NC', 'North Carolina'),
('ND', 'North Dakota'),
('OH', 'Ohio'),
('OK', 'Oklahoma'),
('OR', 'Oregon'),
('PA', 'Pennsylvania'),
('RI', 'Rhode Island'),
('SC', 'South Carolina'),
('SD', 'South Dakota'),
('TN', 'Tennessee'),
('TX', 'Texas'),
('UT', 'Utah'),
('VT', 'Vermont'),
('VA', 'Virginia'),
('WA', 'Washington'),
('WV', 'West Virginia'),
('WI', 'Wisconsin'),
('WY', 'Wyoming');

INSERT INTO flights (departure_state, arrival_state, departure_time, arrival_time, price)  
SELECT s1.state_name, s2.state_name,
(NOW() + INTERVAL '1 day' * FLOOR(RANDOM() * 30))::DATE + TIME '00:00:00' + INTERVAL '1 hour' * FLOOR(RANDOM() * 23),
(NOW() + INTERVAL '1 day' * FLOOR(RANDOM() * 30))::DATE + TIME '00:00:00' + INTERVAL '1 hour' * FLOOR(RANDOM() * 23),
CAST((RANDOM()  * 500 + 50) AS NUMERIC(10,2))
FROM states s1
CROSS JOIN states s2
WHERE s1.state_name <> s2.state_name;

SELECT * FROM flights

UPDATE flights
SET arrival_time = departure_time, departure_time = arrival_time
WHERE arrival_time < departure_time;