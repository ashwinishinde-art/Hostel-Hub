# 🗄️ MySQL Setup & Troubleshooting

## ❌ Error You Got
```
Can't connect to local server through socket '/run/mysqld/mysqld.sock' (2)
```

**Meaning:** MySQL service is not running.

---

## ✅ Solution: Start MySQL

### **For Linux/WSL (Ubuntu/Debian):**

```bash
# Start MySQL service
sudo service mysql start

# Or using systemctl
sudo systemctl start mysql

# Check if it's running
sudo systemctl status mysql
```

### **Alternative - Check MySQL status:**
```bash
ps aux | grep mysql
```

Should show mysql process running.

---

## 🔧 If MySQL is Already Running

Try this to verify:
```bash
mysql -u root -e "SELECT 1;"
```

If successful, you'll see:
```
+---+
| 1 |
+---+
| 1 |
+---+
```

---

## 📋 Complete Startup Sequence

**Terminal 1 - Start MySQL:**
```bash
sudo service mysql start
```

**Terminal 2 - Verify MySQL:**
```bash
mysql -u root -e "SELECT 1;"
```

**Terminal 3 - Run Flask App:**
```bash
cd /home/prajwal/Programs/Hostel
python app.py
```

**Terminal 4 - Open Browser:**
```
http://10.252.129.72:5000
```

---

## 🎯 Common MySQL Commands

```bash
# Start MySQL
sudo service mysql start

# Stop MySQL
sudo service mysql stop

# Restart MySQL
sudo service mysql restart

# Check status
sudo systemctl status mysql

# View MySQL logs (if issues)
sudo tail -f /var/log/mysql/error.log
```

---

## ✨ Once MySQL is Running

Flask will:
1. Connect to MySQL automatically
2. Load the hostel_management database
3. Start serving on port 5000
4. Show: ✅ Database connected successfully!

---

## ⚠️ If Still Having Issues

Check MySQL installation:
```bash
which mysql
mysql --version
```

If not installed:
```bash
sudo apt-get install mysql-server
```

---

**Now go back and run `python app.py` after starting MySQL!**
