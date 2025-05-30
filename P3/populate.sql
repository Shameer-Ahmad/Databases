-- Insert default owner
INSERT INTO user (username, password, role, is_logged)
VALUES ('default_owner', 'default123', 'owner', 0);


-- Insert data into neighborhood_zip table
INSERT INTO neighborhood_zip (zip_code, neighborhood)
VALUES 
('02113', 'North End'),
('02215', 'Fenway'),
('02116', 'Back Bay'),
('02139', 'Central Square'),
('02127', 'South Boston'),
('02130', 'Jamaica Plain'),
('02134', 'Allston'),
('02119', 'Roxbury'),
('02129', 'Charlestown');


-- Insert data into restaurant table
INSERT INTO restaurant (restaurant_name, street_number, street_name, apt_number, city, state, zip_code, cuisine_type, user_id)
VALUES 
('North End Pasta', '123', 'Hanover St', NULL, 'Boston', 'MA', '02113', 'Italian', 1),
('Beacon Burgers', '456', 'Beacon St', NULL, 'Boston', 'MA', '02215', 'American', 1),
('Back Bay Sushi', '789', 'Boylston St', NULL, 'Boston', 'MA', '02116', 'Japanese', 1),
('Fenway Tacos', '111', 'Brookline Ave', NULL, 'Boston', 'MA', '02215', 'Mexican', 1),
('Cambridge Curry', '222', 'Massachusetts Ave', '2B', 'Cambridge', 'MA', '02139', 'Indian', 1),
('Southie Seafood', '333', 'L St', NULL, 'Boston', 'MA', '02127', 'Seafood', 1),
('Jamaica Java', '444', 'Centre St', NULL, 'Boston', 'MA', '02130', 'Cafe', 1),
('Allston Wok', '555', 'Harvard Ave', NULL, 'Boston', 'MA', '02134', 'Chinese', 1),
('Roxbury Ramen', '666', 'Warren St', NULL, 'Boston', 'MA', '02119', 'Japanese', 1),
('Charlestown Chops', '777', 'Main St', NULL, 'Boston', 'MA', '02129', 'Steakhouse', 1);
