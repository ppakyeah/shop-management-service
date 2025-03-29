-- 테스트 데이터베이스에 대한 권한 부여
CREATE DATABASE IF NOT EXISTS shop_management_test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
GRANT ALL PRIVILEGES ON shop_management_test.* TO 'mysql'@'%';
GRANT ALL PRIVILEGES ON `test\_%`.* TO 'mysql'@'%';
FLUSH PRIVILEGES; 