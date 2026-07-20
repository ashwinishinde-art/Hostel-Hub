-- Migration: Add gender field to track boys/girls for room separation
-- This allows us to prevent girls and boys from sharing the same room

ALTER TABLE users ADD COLUMN gender ENUM('Male', 'Female') NULL;

ALTER TABLE rooms ADD COLUMN gender_occupancy ENUM('Boys', 'Girls', 'Mixed') DEFAULT 'Mixed';

-- Update existing sample data with gender information
-- Boys
UPDATE users SET gender = 'Male' WHERE username IN ('admin', 'prajwal', 'rajdeep', 'warden');

-- Girls
UPDATE users SET gender = 'Female' WHERE username IN ('rutuja');

-- Mark existing rooms based on current occupants (can be updated later by admin)
-- For now, mark all as Mixed until admin decides
UPDATE rooms SET gender_occupancy = 'Mixed';
