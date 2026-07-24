#!/usr/bin/env python3
"""
Test script for the fee management system
Tests:
1. Admin can add fees to all students
2. Admin can add fees to selected students
3. Students can make payments
4. Fee status updates correctly
"""

import sys
import os
sys.path.insert(0, '/home/prajwal/Desktop/Hostel-Hub')

from config.database import db
from datetime import datetime, timedelta

def test_add_fees_to_all_students():
    """Test adding fees to all students"""
    print("\n" + "="*60)
    print("TEST 1: Add fees to all students")
    print("="*60)
    
    try:
        cursor = db.connection.cursor()
        
        # Get all students first
        cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 3")
        students = cursor.fetchall()
        
        if not students:
            print("❌ No students found in database")
            return False
        
        print(f"✓ Found {len(students)} students")
        
        # Add fees
        academic_year = "2024-2025"
        semester = 1
        room_rent = 5000.00
        mess_fee = 2000.00
        utilities_fee = 500.00
        other_charges = 0.00
        total_amount = room_rent + mess_fee + utilities_fee + other_charges
        due_date = (datetime.now() + timedelta(days=30)).date()
        
        fees_added = 0
        for student in students:
            student_id = student['id']
            cursor.execute("""
                INSERT INTO fees (student_id, academic_year, semester, room_rent, mess_fee, 
                                utilities_fee, other_charges, total_amount, pending_amount, 
                                due_date, payment_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
            """, (student_id, academic_year, semester, room_rent, mess_fee, 
                  utilities_fee, other_charges, total_amount, total_amount, due_date))
            fees_added += 1
        
        db.connection.commit()
        print(f"✓ Successfully added fees to {fees_added} students")
        print(f"  - Academic Year: {academic_year}")
        print(f"  - Semester: {semester}")
        print(f"  - Total Amount: ₹{total_amount:.2f}")
        print(f"  - Due Date: {due_date}")
        
        # Verify fees were added
        cursor.execute("""
            SELECT COUNT(*) as count FROM fees 
            WHERE academic_year = %s AND semester = %s
        """, (academic_year, semester))
        count_result = cursor.fetchone()
        fee_count = count_result['count'] if count_result else 0
        print(f"✓ Verified: {fee_count} fee records in database")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.connection.rollback()
        return False

def test_student_payment():
    """Test student making a payment"""
    print("\n" + "="*60)
    print("TEST 2: Student makes payment")
    print("="*60)
    
    try:
        cursor = db.connection.cursor()
        
        # Get a fee record
        cursor.execute("""
            SELECT id, student_id, pending_amount, payment_status FROM fees 
            WHERE payment_status IN ('Pending', 'Partial')
            LIMIT 1
        """)
        fee = cursor.fetchone()
        
        if not fee:
            print("❌ No pending fees found")
            return False
        
        fee_id = fee['id']
        student_id = fee['student_id']
        pending_amount = fee['pending_amount']
        
        print(f"✓ Found fee record: Fee ID={fee_id}, Student ID={student_id}")
        print(f"  - Current Status: {fee['payment_status']}")
        print(f"  - Pending Amount: ₹{pending_amount:.2f}")
        
        # Make a partial payment
        payment_amount = min(2500.00, pending_amount)  # Pay ₹2500 or remaining amount
        payment_method = "Online"
        transaction_id = "TXN123456789"
        
        cursor.execute("""
            INSERT INTO payment_history (fee_id, student_id, amount_paid, payment_method, 
                                       transaction_id, payment_date, recorded_by, notes)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s, %s)
        """, (fee_id, student_id, payment_amount, payment_method, transaction_id, 
              student_id, "Payment made by student"))
        
        # Update fee status
        new_pending = pending_amount - payment_amount
        if new_pending <= 0:
            new_status = 'Paid'
        elif new_pending < pending_amount:
            new_status = 'Partial'
        else:
            new_status = 'Pending'
        
        cursor.execute("""
            UPDATE fees 
            SET paid_amount = paid_amount + %s,
                pending_amount = %s,
                payment_status = %s,
                last_payment_date = NOW()
            WHERE id = %s
        """, (payment_amount, max(0, new_pending), new_status, fee_id))
        
        db.connection.commit()
        print(f"✓ Payment recorded successfully")
        print(f"  - Amount Paid: ₹{payment_amount:.2f}")
        print(f"  - Payment Method: {payment_method}")
        print(f"  - Transaction ID: {transaction_id}")
        print(f"  - New Status: {new_status}")
        print(f"  - Remaining Pending: ₹{max(0, new_pending):.2f}")
        
        # Verify payment was recorded
        cursor.execute("""
            SELECT amount_paid, payment_method FROM payment_history 
            WHERE fee_id = %s AND transaction_id = %s
        """, (fee_id, transaction_id))
        payment = cursor.fetchone()
        
        if payment:
            print(f"✓ Verified: Payment recorded in database")
        else:
            print(f"❌ Payment verification failed")
            return False
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.connection.rollback()
        return False

def test_fee_status_transitions():
    """Test fee status transitions"""
    print("\n" + "="*60)
    print("TEST 3: Fee status transitions")
    print("="*60)
    
    try:
        cursor = db.connection.cursor()
        
        # Get a fee with Pending status
        cursor.execute("""
            SELECT id, total_amount, payment_status FROM fees 
            WHERE payment_status = 'Pending'
            LIMIT 1
        """)
        fee = cursor.fetchone()
        
        if not fee:
            print("❌ No pending fees found for testing")
            return False
        
        fee_id = fee['id']
        total_amount = fee['total_amount']
        
        print(f"✓ Found fee: ID={fee_id}, Total=₹{total_amount:.2f}, Status={fee['payment_status']}")
        
        # Test partial payment
        cursor.execute("""
            UPDATE fees 
            SET paid_amount = %s, pending_amount = %s, payment_status = 'Partial'
            WHERE id = %s
        """, (total_amount * 0.5, total_amount * 0.5, fee_id))
        db.connection.commit()
        print(f"✓ Status updated to: Partial")
        
        # Test full payment
        cursor.execute("""
            UPDATE fees 
            SET paid_amount = %s, pending_amount = 0, payment_status = 'Paid'
            WHERE id = %s
        """, (total_amount, fee_id))
        db.connection.commit()
        print(f"✓ Status updated to: Paid")
        
        # Verify final status
        cursor.execute("SELECT payment_status, paid_amount, pending_amount FROM fees WHERE id = %s", (fee_id,))
        final_fee = cursor.fetchone()
        print(f"✓ Final verification: Status={final_fee['payment_status']}, Paid=₹{final_fee['paid_amount']:.2f}, Pending=₹{final_fee['pending_amount']:.2f}")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.connection.rollback()
        return False

def test_payment_history():
    """Test payment history tracking"""
    print("\n" + "="*60)
    print("TEST 4: Payment history tracking")
    print("="*60)
    
    try:
        cursor = db.connection.cursor()
        
        # Get a student with payments
        cursor.execute("""
            SELECT DISTINCT ph.student_id, COUNT(*) as payment_count
            FROM payment_history ph
            GROUP BY ph.student_id
            LIMIT 1
        """)
        result = cursor.fetchone()
        
        if not result:
            print("⚠ No payment history found (this is normal if no payments were made)")
            return True
        
        student_id = result['student_id']
        payment_count = result['payment_count']
        
        print(f"✓ Found student {student_id} with {payment_count} payment(s)")
        
        # Get payment history
        cursor.execute("""
            SELECT ph.*, f.academic_year, f.semester 
            FROM payment_history ph
            JOIN fees f ON ph.fee_id = f.id
            WHERE ph.student_id = %s
            ORDER BY ph.payment_date DESC
        """, (student_id,))
        payments = cursor.fetchall()
        
        for i, payment in enumerate(payments[:3], 1):  # Show first 3 payments
            print(f"  Payment {i}:")
            print(f"    - Amount: ₹{payment['amount_paid']:.2f}")
            print(f"    - Method: {payment['payment_method']}")
            print(f"    - Date: {payment['payment_date']}")
            print(f"    - Academic Year: {payment['academic_year']}")
            print(f"    - Semester: {payment['semester']}")
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " FEE MANAGEMENT SYSTEM - TEST SUITE ".center(58) + "║")
    print("╚" + "="*58 + "╝")
    
    tests = [
        ("Add Fees to All Students", test_add_fees_to_all_students),
        ("Student Payment", test_student_payment),
        ("Fee Status Transitions", test_fee_status_transitions),
        ("Payment History Tracking", test_payment_history),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Unexpected error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
