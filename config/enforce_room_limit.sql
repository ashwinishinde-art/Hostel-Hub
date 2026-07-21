-- Add a UNIQUE constraint to prevent duplicate room numbers
-- This ensures room numbers are unique across the system
ALTER TABLE rooms ADD CONSTRAINT unique_room_number UNIQUE (room_number);

-- Add CHECK constraint to enforce max 5 rooms per floor
-- Note: This will be enforced via application logic as MySQL CHECK constraints may not work 
-- as expected in all versions, but we add this for database-level constraint

-- Create a trigger to enforce max 5 rooms per floor
DELIMITER $$

DROP TRIGGER IF EXISTS check_max_rooms_per_floor_insert$$

CREATE TRIGGER check_max_rooms_per_floor_insert
BEFORE INSERT ON rooms
FOR EACH ROW
BEGIN
    DECLARE room_count INT;
    
    -- Count existing rooms on this floor
    SELECT COUNT(*) INTO room_count FROM rooms WHERE floor = NEW.floor;
    
    -- If already 5 rooms on this floor, raise an error
    IF room_count >= 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Maximum 5 rooms allowed per floor';
    END IF;
END$$

DROP TRIGGER IF EXISTS check_max_rooms_per_floor_update$$

CREATE TRIGGER check_max_rooms_per_floor_update
BEFORE UPDATE ON rooms
FOR EACH ROW
BEGIN
    DECLARE room_count INT;
    
    -- If floor is being changed, check if new floor would exceed limit
    IF NEW.floor != OLD.floor THEN
        SELECT COUNT(*) INTO room_count FROM rooms WHERE floor = NEW.floor;
        
        IF room_count >= 5 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Maximum 5 rooms allowed per floor';
        END IF;
    END IF;
END$$

DELIMITER ;

-- Display current rooms per floor (for verification)
SELECT floor, COUNT(*) as room_count FROM rooms GROUP BY floor ORDER BY floor;
