INSERT INTO user (username, password, role, is_logged)
VALUES ('default_owner', 'default123', 'owner', 0);

INSERT INTO restaurant (restaurant_name, street_number, street_name, apt_number, city, state, zip_code, cuisine_type, user_id)
VALUES 
('North End Pasta', '123', 'Hanover St', NULL, 'North End', 'MA', '02113', 'Italian', 1),
('Beacon Burgers', '456', 'Beacon St', NULL, 'Beacon Hill', 'MA', '02215', 'American', 1),
('Back Bay Sushi', '789', 'Boylston St', NULL, 'Back Bay', 'MA', '02116', 'Japanese', 1),
('Fenway Tacos', '111', 'Brookline Ave', NULL, 'Fenway', 'MA', '02215', 'Mexican', 1),
('Cambridge Curry', '222', 'Massachusetts Ave', '2B', 'Cambridge', 'MA', '02139', 'Indian', 1),
('Southie Seafood', '333', 'L St', NULL, 'Southie', 'MA', '02127', 'Seafood', 1),
('Jamaica Java', '444', 'Centre St', NULL, 'Jamaica Plain', 'MA', '02130', 'Cafe', 1),
('Allston Wok', '555', 'Harvard Ave', NULL, 'Allston', 'MA', '02134', 'Chinese', 1),
('Roxbury Ramen', '666', 'Warren St', NULL, 'Roxbury', 'MA', '02119', 'Japanese', 1),
('Charlestown Chops', '777', 'Main St', NULL, 'Charlestown', 'MA', '02129', 'Steakhouse', 1);