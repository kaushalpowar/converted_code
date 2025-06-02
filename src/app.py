#!/usr/bin/env python3
"""
Investment Appointment Management System

This module provides functionality for managing investment appointments related to insurance policies.
It allows users to add, modify, cancel, and query investment appointments.

Original program: ps917m.4gl
Author: epf
Date: 104/04/08
Process: Insurance policy investment appointment
"""

import datetime
import logging
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class ProcessType(Enum):
    """Process type enumeration."""
    ADD = "1"
    CANCEL = "2"
    MODIFY = "3"
    QUERY = "4"


class AppointmentType(Enum):
    """Appointment type enumeration."""
    CONVERSION = "1"  # Investment conversion
    WITHDRAWAL = "2"  # Investment withdrawal


class FrequencyType(Enum):
    """Frequency type enumeration."""
    ONCE = 0       # One-time
    MONTHLY = 1    # Monthly
    QUARTERLY = 3  # Quarterly
    SEMI_ANNUAL = 6  # Semi-annual
    ANNUAL = 12    # Annual


class SellType(Enum):
    """Sell type enumeration."""
    AMOUNT = "1"   # Sell by amount
    ALL = "2"      # Sell all


class DisbursementType(Enum):
    """Disbursement type enumeration."""
    BANK_TRANSFER = "0"  # Bank transfer
    PERSONAL_ACCOUNT = "1"  # Personal account
    POLICY_ACCOUNT = "2"  # Policy account


class ActiveStatus(Enum):
    """Active status enumeration."""
    PENDING = " "  # Pending
    ACTIVE = "0"   # Active
    CANCELLED = "1"  # Cancelled
    EXPIRED = "2"  # Expired


@dataclass
class PolicyInfo:
    """Policy information."""
    policy_no: str = ""
    po_sts_code: str = ""
    currency: str = ""
    basic_plan_code: str = ""
    insurance_type: str = ""
    basic_rate_scale: str = ""


@dataclass
class ClientInfo:
    """Client information."""
    owner_id: str = ""
    o1_name: str = ""
    client_id: str = ""
    names: str = ""


@dataclass
class DisplayInfo:
    """Display information."""
    receive_date: str = ""
    c_desc: str = ""
    po_chg_code: str = ""
    owner_id: str = ""
    o1_name: str = ""
    client_id: str = ""
    names: str = ""
    new_receive_no: str = ""


@dataclass
class PlanInfo:
    """Plan information."""
    part_wd_amt_mini: float = 0.0
    invs_avail_type: str = ""
    iv_ass_array: str = ""
    ivchg_array: str = ""


@dataclass
class InvestmentInfo:
    """Investment information."""
    invs_code: str = ""
    invs_title: str = ""
    invs_sts_code: str = ""
    currency: str = ""
    invs_risk_degree: str = ""


@dataclass
class SellRecord:
    """Sell record information."""
    invs_code: str = ""
    chah_sell_type: str = ""
    chah_sell_type_desc: str = ""
    invs_ad_amt: float = 0.0
    skip_field: str = ""


@dataclass
class BuyRecord:
    """Buy record information."""
    invs_code: str = ""
    invs_ad_perc: float = 0.0


@dataclass
class AppointmentHeader:
    """Appointment header information."""
    chah_seq: int = 0
    policy_no: str = ""
    receive_no: str = ""
    chah_ind: str = ""
    chah_freq: int = 0
    bgn_date: str = ""
    auto_tr_date: str = ""
    currency: str = ""
    active_ind: str = ""
    process_user: str = ""
    process_date: str = ""
    process_time: str = ""


@dataclass
class AppointmentPayment:
    """Appointment payment information."""
    chah_seq: int = 0
    policy_no: str = ""
    receive_no: str = ""
    chap_disb_type: str = ""
    remit_bank: str = ""
    remit_branch: str = ""
    remit_account: str = ""
    payee: str = ""
    payee_e: str = ""
    payee_id: str = ""
    swift_code: str = ""
    bank_name_e: str = ""
    bank_address_e: str = ""


@dataclass
class InvestmentAppointmentSystem:
    """Investment Appointment System main class."""
    process_ind: str = ""
    policy_info: PolicyInfo = field(default_factory=PolicyInfo)
    client_info: ClientInfo = field(default_factory=ClientInfo)
    display_info: DisplayInfo = field(default_factory=DisplayInfo)
    plan_info: PlanInfo = field(default_factory=PlanInfo)
    appointment_header: AppointmentHeader = field(default_factory=AppointmentHeader)
    appointment_payment: AppointmentPayment = field(default_factory=AppointmentPayment)
    sell_records: List[SellRecord] = field(default_factory=list)
    buy_records: List[BuyRecord] = field(default_factory=list)
    
    # System variables
    user_id: str = ""
    user_dept: str = ""
    today: str = ""
    last_work_date: str = ""
    total_record: int = 0
    current_record: int = 0
    is_new: bool = False
    chah_ind: str = "1"  # Default to conversion
    check_amt_ind: bool = True
    sell_sum_amt: float = 0.0
    
    def __post_init__(self):
        """Initialize after creation."""
        self.today = self.get_date(datetime.date.today())
        self.last_work_date = self.get_last_work_date(self.today, 1)
        self.user_id = self.get_current_user()
        self.user_dept = self.get_user_department()
    
    def get_date(self, date_obj: datetime.date) -> str:
        """
        Convert a datetime.date object to a string in the format 'YYY/MM/DD'.
        
        Args:
            date_obj: The date object to convert
            
        Returns:
            A string representation of the date
        """
        # Format: YYY/MM/DD (Taiwan calendar format)
        year = date_obj.year - 1911  # Convert to Taiwan calendar
        return f"{year:03d}/{date_obj.month:02d}/{date_obj.day:02d}"
    
    def get_last_work_date(self, date_str: str, days_back: int) -> str:
        """
        Get the last working date before the given date.
        
        Args:
            date_str: The reference date string
            days_back: Number of working days to go back
            
        Returns:
            The last working date as a string
        """
        # This is a simplified implementation
        # In a real system, this would check holidays and weekends
        date_parts = date_str.split('/')
        year = int(date_parts[0]) + 1911  # Convert from Taiwan calendar
        month = int(date_parts[1])
        day = int(date_parts[2])
        
        date_obj = datetime.date(year, month, day)
        prev_date = date_obj - datetime.timedelta(days=days_back)
        
        return self.get_date(prev_date)
    
    def get_current_user(self) -> str:
        """Get the current user ID."""
        # In a real system, this would get the user from the session
        return "SYSTEM"
    
    def get_user_department(self) -> str:
        """Get the department of the current user."""
        # In a real system, this would query the database
        return "IT"
    
    def check_authority(self, operation_type: str, show_error: bool = False) -> bool:
        """
        Check if the current user has authority to perform the operation.
        
        Args:
            operation_type: The type of operation ('C', 'U', 'D', 'Q')
            show_error: Whether to show an error message if not authorized
            
        Returns:
            True if authorized, False otherwise
        """
        # In a real system, this would check user permissions
        return True
    
    def set_input_form(self, is_new: bool) -> None:
        """
        Set up the input form based on the appointment type.
        
        Args:
            is_new: Whether this is a new form
        """
        logger.info(f"Setting up form for appointment type: {self.chah_ind}")
        # In a GUI system, this would set up the appropriate form
    
    def show_logo(self) -> None:
        """Display the application logo."""
        logger.info("Displaying application logo")
        # In a GUI system, this would display the logo
    
    def job_control(self) -> None:
        """Initialize job control."""
        logger.info("Initializing job control")
        # In a real system, this would initialize job control parameters
    
    def main(self) -> None:
        """Main function to run the application."""
        self.show_logo()
        self.job_control()
        
        while True:
            print("\nInvestment Appointment Management System")
            print("1) Add")
            print("2) Cancel")
            print("3) Modify")
            print("4) Query")
            print("0) Exit")
            
            choice = input("Select an option: ")
            
            if choice == "1" and self.check_authority("C"):
                self.process_ind = ProcessType.ADD.value
                self.appoint_add()
            elif choice == "2" and self.check_authority("U"):
                self.process_ind = ProcessType.CANCEL.value
                self.appoint_cancel()
            elif choice == "3" and self.check_authority("D"):
                self.process_ind = ProcessType.MODIFY.value
                self.appoint_modify()
            elif choice == "4" and self.check_authority("Q"):
                self.process_ind = ProcessType.QUERY.value
                self.appoint_query()
            elif choice == "0":
                break
            else:
                print("Invalid option or insufficient permissions.")
        
        print("Exiting application.")
    
    def show_total_record(self) -> None:
        """Display the total number of records."""
        print(f"Total records: {self.total_record}")
    
    def show_current_record(self) -> None:
        """Display the current record number."""
        print(f"Current record: {self.current_record} of {self.total_record}")
    
    def display_appointment(self) -> None:
        """Display the appointment information."""
        print("\n=== Appointment Information ===")
        print(f"Policy No: {self.appointment_header.policy_no}")
        print(f"Policy Status: {self.policy_info.po_sts_code}")
        print(f"Receive No: {self.appointment_header.receive_no}")
        print(f"Receive Date: {self.display_info.receive_date}")
        print(f"Active Status: {self.appointment_header.active_ind}")
        print(f"Frequency: {self.appointment_header.chah_freq}")
        print(f"Appointment Type: {self.appointment_header.chah_ind}")
        print(f"Begin Date: {self.appointment_header.bgn_date}")
        print(f"Currency: {self.policy_info.currency}")
        print(f"Currency Description: {self.display_info.c_desc}")
        print(f"Basic Plan Code: {self.policy_info.basic_plan_code}")
        print(f"Owner Name: {self.display_info.o1_name}")
        print(f"Insured Name: {self.display_info.names}")
        
        if self.process_ind == ProcessType.CANCEL.value:
            print(f"New Receive No: {self.display_info.new_receive_no}")
    
    def display_remit_data(self) -> None:
        """Display remittance data."""
        print("\n=== Remittance Information ===")
        bank_name = self.get_bank_name(
            f"{self.appointment_payment.remit_bank}{self.appointment_payment.remit_branch}"
        )
        
        print(f"Disbursement Type: {self.appointment_payment.chap_disb_type}")
        print(f"Bank: {self.appointment_payment.remit_bank}")
        print(f"Branch: {self.appointment_payment.remit_branch}")
        print(f"Bank Name: {bank_name}")
        print(f"Account: {self.appointment_payment.remit_account}")
        print(f"Payee: {self.appointment_payment.payee}")
        print(f"Payee (English): {self.appointment_payment.payee_e}")
    
    def display_sell(self, start_index: int) -> None:
        """
        Display sell records starting from the given index.
        
        Args:
            start_index: The starting index (1-based)
        """
        print("\n=== Sell Records ===")
        
        end_index = min(start_index + 2, len(self.sell_records))
        for i in range(start_index - 1, end_index):
            record = self.sell_records[i]
            sell_type_desc = self.get_term_meaning("chah_sell_type", record.chah_sell_type)
            print(f"{i+1}. Code: {record.invs_code}, Type: {sell_type_desc}, Amount: {record.invs_ad_amt}")
        
        print(f"Total sell records: {len(self.sell_records)}")
    
    def display_buy(self, start_index: int) -> None:
        """
        Display buy records starting from the given index.
        
        Args:
            start_index: The starting index (1-based)
        """
        print("\n=== Buy Records ===")
        
        end_index = min(start_index + 2, len(self.buy_records))
        for i in range(start_index - 1, end_index):
            record = self.buy_records[i]
            print(f"{i+1}. Code: {record.invs_code}, Percentage: {record.invs_ad_perc}%")
        
        print(f"Total buy records: {len(self.buy_records)}")
    
    def ask_policy_no(self) -> bool:
        """
        Ask for policy number and receive number.
        
        Returns:
            True if successful, False otherwise
        """
        print("\nEnter Policy Number or Receive Number (Esc to cancel, End to finish):")
        
        try:
            self.appointment_header.policy_no = input("Policy Number: ")
            if not self.appointment_header.policy_no:
                return False
            
            # Check policy number validation
            if not self.check_policy_no(self.appointment_header.policy_no):
                print("Invalid policy number checksum. Please correct.")
                return False
            
            # Read transaction data (using the largest receive number)
            self.appointment_header.receive_no = self.get_latest_receive_no(self.appointment_header.policy_no)
            if not self.appointment_header.receive_no:
                print("No transaction data found for this policy.")
                return False
            
            self.display_info.receive_date = self.get_receive_date(self.appointment_header.receive_no)
            self.display_info.po_chg_code = self.get_po_chg_code(self.appointment_header.receive_no)
            
            if self.process_ind == ProcessType.CANCEL.value:
                self.display_info.new_receive_no = self.appointment_header.receive_no
            
            print(f"Policy No: {self.appointment_header.policy_no}")
            print(f"Receive No: {self.appointment_header.receive_no}")
            print(f"Receive Date: {self.display_info.receive_date}")
            
            # Check if the policy meets investment conditions
            if not self.check_invest_condition():
                return False
            
            # Load data
            self.loading_data()
            
            # Check policy conditions
            return self.check_policy_condition()
            
        except KeyboardInterrupt:
            return False
    
    def check_policy_no(self, policy_no: str) -> bool:
        """
        Check if the policy number is valid.
        
        Args:
            policy_no: The policy number to check
            
        Returns:
            True if valid, False otherwise
        """
        # In a real system, this would validate the policy number checksum
        return len(policy_no) > 0
    
    def get_latest_receive_no(self, policy_no: str) -> str:
        """
        Get the latest receive number for the policy.
        
        Args:
            policy_no: The policy number
            
        Returns:
            The latest receive number
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT FIRST 1 a.po_chg_rece_no, a.po_chg_rece_date, b.po_chg_code
        # FROM apdt a, apit b
        # WHERE a.po_chg_rece_no = b.po_chg_rece_no
        # AND a.policy_no = policy_no
        # AND a.po_chg_sts_code MATCHES "[2]"
        # AND b.po_chg_code IN ('73','74')
        # ORDER BY 1 DESC
        
        # Simulated response
        return "R12345678"
    
    def get_receive_date(self, receive_no: str) -> str:
        """
        Get the receive date for the given receive number.
        
        Args:
            receive_no: The receive number
            
        Returns:
            The receive date
        """
        # In a real system, this would query the database
        return self.today
    
    def get_po_chg_code(self, receive_no: str) -> str:
        """
        Get the policy change code for the given receive number.
        
        Args:
            receive_no: The receive number
            
        Returns:
            The policy change code
        """
        # In a real system, this would query the database
        return "73"  # Default to conversion
    
    def select_data(self) -> bool:
        """
        Select data based on search criteria.
        
        Returns:
            True if data found, False otherwise
        """
        print("\nEnter search criteria (Esc to cancel, End to finish):")
        
        try:
            # In a real system, this would be a form for entering search criteria
            policy_no = input("Policy Number (optional): ")
            receive_no = input("Receive Number (optional): ")
            chah_ind = input("Appointment Type (optional, 1=Conversion, 2=Withdrawal): ")
            active_ind = input("Active Status (optional): ")
            bgn_date = input("Begin Date (optional): ")
            chah_freq = input("Frequency (optional): ")
            
            # Build search criteria
            criteria = []
            if policy_no:
                self.appointment_header.policy_no = policy_no
                criteria.append(f"policy_no = '{policy_no}'")
            if receive_no:
                self.appointment_header.receive_no = receive_no
                criteria.append(f"receive_no = '{receive_no}'")
            if chah_ind:
                criteria.append(f"chah_ind = '{chah_ind}'")
                self.chah_ind = chah_ind
            if active_ind:
                criteria.append(f"active_ind = '{active_ind}'")
            if bgn_date:
                criteria.append(f"bgn_date = '{bgn_date}'")
            if chah_freq:
                criteria.append(f"chah_freq = {chah_freq}")
            
            if self.process_ind in [ProcessType.ADD.value, ProcessType.MODIFY.value, ProcessType.CANCEL.value]:
                if not self.appointment_header.policy_no and not self.appointment_header.receive_no:
                    print("Please enter at least Policy Number or Receive Number!")
                    return False
            
            if self.process_ind == ProcessType.QUERY.value and not criteria:
                print("Please enter at least one search criterion!")
                return False
            
            # Count matching records
            # In a real system, this would query the database
            self.total_record = 1  # Simulated count
            
            if self.total_record == 0:
                print("No matching records found.")
                return False
            
            return True
            
        except KeyboardInterrupt:
            return False
    
    def appoint_add(self) -> None:
        """Add a new appointment."""
        self.appointment_header = AppointmentHeader()
        
        if not self.ask_policy_no():
            return
        
        if not self.initialization(False):
            return
        
        self.display_appointment()
        self.display_sell(1)
        
        if self.chah_ind == AppointmentType.CONVERSION.value:
            self.display_buy(1)
        else:
            self.display_remit_data()
        
        # Edit and save
        if self.editor_appointment():
            self.appointment_header.process_user = self.user_id
            self.appointment_header.process_date = self.today
            self.appointment_header.process_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            self.display_appointment()
            
            print("\n1: Return to edit  2: Save  3: Approve  Other: Exit")
            ans = input("Please select a function: ")
            
            if ans == "1":
                # Return to edit
                self.appoint_add()
                return
            
            if ans in ["2", "3"]:
                # Check if user is the owner
                if not self.check_owner():
                    print("You are not the owner. Cannot process!")
                    return
                
                # Check authorization
                if ans == "3" and not self.check_authorization(self.appointment_header.receive_no, "44", 0):
                    return
                
                # Save data
                try:
                    if self.is_new:
                        self.inserting_chah()
                        self.inserting_chad()
                    else:
                        self.updating_chah()
                        self.deleting_chad()
                        self.inserting_chad()
                    
                    if not self.check_duplicate_appointment_sell(0):
                        print("Duplicate investment in another appointment conversion/withdrawal!")
                        return
                    
                    print("Data saved successfully.")
                    
                    if ans == "3":
                        self.saving_approval()
                        
                        # Insert print record
                        if not self.psrd_insert(self.appointment_header.receive_no):
                            print("Error inserting print record.")
                        
                        # Show print record
                        self.query_psrd(self.appointment_header.receive_no)
                        
                        # Print policy letter
                        input("Print policy letter (press Enter to confirm): ")
                        if not self.insert_pble(self.appointment_header.policy_no, 
                                              self.appointment_header.receive_no, 'PL'):
                            pass  # Error handling
                        
                        # Print policy documents
                        print_option = input("Print policy documents (1.Letter 2.Certificate 3.Both): ")
                        success = True
                        
                        if print_option in ["1", "3"]:
                            success = self.print_po_only(self.appointment_header.policy_no, 
                                                       self.appointment_header.receive_no, '1')
                        
                        if print_option in ["2", "3"]:
                            success = self.print_po_only(self.appointment_header.policy_no, 
                                                       self.appointment_header.receive_no, '2')
                        
                        if not success:
                            print("Error printing policy documents.")
                        
                        # Update transaction status
                        self.update_transaction_status(self.appointment_header.receive_no, "C")
                        self.update_transaction_status(self.appointment_header.receive_no, "5")
                        
                        print("Data approved successfully.")
                
                except Exception as e:
                    print(f"Error saving data: {e}")
        else:
            print("Addition cancelled.")
    
    def appoint_cancel(self) -> None:
        """Cancel an appointment."""
        self.appointment_header = AppointmentHeader()
        cancel_ind = False
        
        if not self.ask_policy_no():
            return
        
        if not self.select_data():
            return
        
        # Count active records
        # In a real system, this would query the database
        self.total_record = 1  # Simulated count
        
        # Load data
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM chah WHERE {criteria} AND active_ind = '0' ORDER BY chah_seq DESC
        
        # Simulated data
        self.current_record = 1
        self.loading_data()
        self.display_appointment()
        self.display_sell(1)
        
        if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
            self.display_buy(1)
        else:
            self.display_remit_data()
        
        self.show_current_record()
        self.show_total_record()
        
        # Navigation menu
        while True:
            print("\nN) Next record  P) Previous record  3) Cancel  0) Exit")
            choice = input("Select an option: ")
            
            if choice.upper() == "N":
                # Next record
                # In a real system, this would fetch the next record
                self.current_record += 1
                if self.current_record > self.total_record:
                    self.current_record = self.total_record
                self.loading_data()
                self.display_appointment()
                self.display_sell(1)
                if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
                    self.display_buy(1)
                else:
                    self.display_remit_data()
                self.show_current_record()
                self.show_total_record()
            
            elif choice.upper() == "P":
                # Previous record
                # In a real system, this would fetch the previous record
                self.current_record -= 1
                if self.current_record < 1:
                    self.current_record = 1
                self.loading_data()
                self.display_appointment()
                self.display_sell(1)
                if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
                    self.display_buy(1)
                else:
                    self.display_remit_data()
                self.show_current_record()
                self.show_total_record()
            
            elif choice == "3":
                cancel_ind = True
                break
            
            elif choice == "0":
                break
        
        if cancel_ind:
            confirm = input("Confirm cancellation? (y/n): ")
            if confirm.lower() == "y":
                # Check authorization
                if not self.check_authorization(self.display_info.new_receive_no, "44", 0):
                    return
                
                self.saving_cancel()
                
                # Insert print record
                if not self.psrd_insert(self.display_info.new_receive_no):
                    print("Error inserting print record.")
                
                # Show print record
                self.query_psrd(self.display_info.new_receive_no)
                
                # Print policy letter
                input("Print policy letter (press Enter to confirm): ")
                if not self.insert_pble(self.appointment_header.policy_no, 
                                      self.display_info.new_receive_no, 'PL'):
                    pass  # Error handling
                
                # Print policy documents
                print_option = input("Print policy documents (1.Letter 2.Certificate 3.Both): ")
                success = True
                
                if print_option in ["1", "3"]:
                    success = self.print_po_only(self.appointment_header.policy_no, 
                                               self.display_info.new_receive_no, '1')
                
                if print_option in ["2", "3"]:
                    success = self.print_po_only(self.appointment_header.policy_no, 
                                               self.display_info.new_receive_no, '2')
                
                if not success:
                    print("Error printing policy documents.")
                
                # Update transaction status
                self.update_transaction_status(self.display_info.new_receive_no, "C")
                self.update_transaction_status(self.display_info.new_receive_no, "5")
                
                print("Appointment cancelled successfully.")
            else:
                print("Cancellation aborted.")
    
    def appoint_modify(self) -> None:
        """Modify an appointment."""
        self.appointment_header = AppointmentHeader()
        modify_ind = False
        
        if not self.select_data():
            return
        
        # Count active records
        # In a real system, this would query the database
        self.total_record = 1  # Simulated count
        
        # Load data
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM chah WHERE {criteria} AND active_ind = '0' ORDER BY chah_seq DESC
        
        # Simulated data
        self.current_record = 1
        self.loading_data()
        self.display_appointment()
        self.display_sell(1)
        
        if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
            self.display_buy(1)
        else:
            self.display_remit_data()
        
        self.show_current_record()
        self.show_total_record()
        
        # Navigation menu
        while True:
            print("\nN) Next record  P) Previous record  3) Modify  0) Exit")
            choice = input("Select an option: ")
            
            if choice.upper() == "N":
                # Next record
                # In a real system, this would fetch the next record
                self.current_record += 1
                if self.current_record > self.total_record:
                    self.current_record = self.total_record
                self.loading_data()
                self.display_appointment()
                self.display_sell(1)
                if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
                    self.display_buy(1)
                else:
                    self.display_remit_data()
                self.show_current_record()
                self.show_total_record()
            
            elif choice.upper() == "P":
                # Previous record
                # In a real system, this would fetch the previous record
                self.current_record -= 1
                if self.current_record < 1:
                    self.current_record = 1
                self.loading_data()
                self.display_appointment()
                self.display_sell(1)
                if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
                    self.display_buy(1)
                else:
                    self.display_remit_data()
                self.show_current_record()
                self.show_total_record()
            
            elif choice == "3":
                modify_ind = True
                break
            
            elif choice == "0":
                break
        
        if modify_ind:
            self.display_appointment()
            self.display_sell(1)
            
            if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
                self.display_buy(1)
            else:
                self.display_remit_data()
            
            # Check if appointment has already started
            if self.check_appointment_started():
                print("This appointment has already started processing. Cannot modify!")
                return
            
            if self.editor_appointment():
                self.appointment_header.process_user = self.user_id
                self.appointment_header.process_date = self.today
                self.appointment_header.process_time = datetime.datetime.now().strftime("%H:%M:%S")
            
            confirm = input("Confirm modification? (y/n): ")
            if confirm.lower() == "y":
                self.saving_modify()
                print("Appointment modified successfully.")
            else:
                print("Modification aborted.")
    
    def appoint_query(self) -> None:
        """Query appointments."""
        if not self.select_data():
            return
        
        # Load data
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM chah WHERE {criteria} ORDER BY chah_seq DESC
        
        # Simulated data
        self.current_record = 1
        self.loading_data()
        self.display_appointment()
        self.display_sell(1)
        
        if self.chah_ind == AppointmentType.CONVERSION.value:
            self.display_buy(1)
        else:
            self.display_remit_data()
        
        self.show_current_record()
        self.show_total_record()
        
        # Navigation menu
        sell_index = 1
        buy_index = 1
        
        while True:
            print("\nN) Next record  P) Previous record  F) First record  E) Last record")
            print("1) Next sell page  2) Previous sell page  3) Next buy page  4) Previous buy page")
            print("0) Exit")
            
            choice = input("Select an option: ")
            
            if choice.upper() == "N":
                # Next record
                # In a real system, this would fetch the next record
                self.current_record += 1
                if self.current_record > self.total_record:
                    self.current_record = self.total_record
                self.loading_data()
                sell_index = 1
                buy_index = 1
                self.display_appointment()
                self.display_sell(sell_index)
                if self.chah_ind == AppointmentType.CONVERSION.value:
                    self.display_buy(buy_index)
                else:
                    self.display_remit_data()
                self.show_current_record()
                self.show_total_record()
            
            elif choice.upper() == "P":
                # Previous record
                # In a real system, this would fetch the previous record
                self.current_record -= 1
                if self.current_record < 1:
                    self.current_record = 1
                self.loading_data()
                sell_index = 1
                buy_index = 1
                self.display_appointment()
                self.display_sell(sell_index)
                if self.chah_ind == AppointmentType.CONVERSION.value:
                    self.display_buy(buy_index)
                else:
                    self.display_remit_data()
                self.show_current_record()
                self.show_total_record()
            
            elif choice.upper() == "F":
                # First record
                # In a real system, this would fetch the first record
                self.current_record = 1
                self.loading_data()
                sell_index = 1
                buy_index = 1
                self.display_appointment()
                self.display_sell(sell_index)
                if self.chah_ind == AppointmentType.CONVERSION.value:
                    self.display_buy(buy_index)
                else:
                    self.display_remit_data()
                self.show_current_record()
                self.show_total_record()
            
            elif choice.upper() == "E":
                # Last record
                # In a real system, this would fetch the last record
                self.current_record = self.total_record
                self.loading_data()
                sell_index = 1
                buy_index = 1
                self.display_appointment()
                self.display_sell(sell_index)
                if self.chah_ind == AppointmentType.CONVERSION.value:
                    self.display_buy(buy_index)
                else:
                    self.display_remit_data()
                self.show_current_record()
                self.show_total_record()
            
            elif choice == "1":
                # Next sell page
                if sell_index + 3 <= len(self.sell_records):
                    sell_index += 3
                    self.display_sell(sell_index)
            
            elif choice == "2":
                # Previous sell page
                if sell_index - 3 > 0:
                    sell_index -= 3
                    self.display_sell(sell_index)
            
            elif choice == "3":
                # Next buy page
                if buy_index + 3 <= len(self.buy_records) and self.chah_ind == AppointmentType.CONVERSION.value:
                    buy_index += 3
                    self.display_buy(buy_index)
            
            elif choice == "4":
                # Previous buy page
                if buy_index - 3 > 0 and self.chah_ind == AppointmentType.CONVERSION.value:
                    buy_index -= 3
                    self.display_buy(buy_index)
            
            elif choice == "0":
                break
    
    def psrd_insert(self, receive_no: str) -> bool:
        """
        Insert print record data.
        
        Args:
            receive_no: The receive number
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # In a real system, this would insert data into the database
            
            # Format date components
            date_parts = self.appointment_header.process_date.split('/')
            yyy = date_parts[0]
            mmm = date_parts[1]
            ddd = date_parts[2]
            
            # Prepare message array
            messages = []
            
            # First line
            messages.append({
                'wt_item': '10',
                'wt_cmnt': f"Policy {self.appointment_header.policy_no} Receive {receive_no} Date {yyy}/{mmm}/{ddd}"
            })
            
            # Second line
            messages.append({
                'wt_item': '42',
                'wt_cmnt': f"Process Date {yyy}/{mmm}/{ddd}"
            })
            
            # Add appointment details
            if self.process_ind == ProcessType.CANCEL.value:
                appointment_type = "Cancel Investment"
            else:
                appointment_type = "Appoint Investment"
                
            if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
                appointment_type += " Conversion"
            else:
                appointment_type += " Withdrawal"
                
            if self.appointment_header.chah_freq == 0:
                appointment_type += f": {yyy} year {mmm} month {ddd} day"
            else:
                appointment_type += f": {yyy} year {mmm} month {ddd} day_Every "
                
                if self.appointment_header.chah_freq == 1:
                    appointment_type += "Month"
                elif self.appointment_header.chah_freq == 3:
                    appointment_type += "Quarter"
                elif self.appointment_header.chah_freq == 6:
                    appointment_type += "Half-year"
                elif self.appointment_header.chah_freq == 12:
                    appointment_type += "Year"
                    
                appointment_type += f" {ddd} day"
            
            # Add original receive number for cancellation
            if self.process_ind == ProcessType.CANCEL.value:
                appointment_type += f"(Original Receive No:{self.appointment_header.receive_no})"
                
            messages.append({
                'wt_item': 'U8',
                'wt_cmnt': appointment_type
            })
            
            # Add sell investment details
            messages.append({
                'wt_item': 'U8',
                'wt_cmnt': "Appointed Sell Investments"
            })
            
            for i, sell in enumerate(self.sell_records):
                investment_title = self.get_investment_title(sell.invs_code)
                sell_detail = f"{sell.invs_code}{investment_title}  "
                
                if sell.chah_sell_type == SellType.AMOUNT.value:
                    sell_detail += f"Sell Amount {sell.invs_ad_amt:.2f}"
                else:
                    sell_detail += "Sell All"
                    
                messages.append({
                    'wt_item': 'U8',
                    'wt_cmnt': sell_detail
                })
            
            # Add buy investment details if conversion
            if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
                messages.append({
                    'wt_item': 'U8',
                    'wt_cmnt': "Appointed Buy Investments"
                })
                
                for i, buy in enumerate(self.buy_records):
                    investment_title = self.get_investment_title(buy.invs_code)
                    buy_detail = f"{buy.invs_code}{investment_title}  Buy Percentage {buy.invs_ad_perc}%"
                    
                    messages.append({
                        'wt_item': 'U8',
                        'wt_cmnt': buy_detail
                    })
            
            # Add final lines
            messages.append({
                'wt_item': 'Z1',
                'wt_cmnt': "Thank you for your business"
            })
            
            messages.append({
                'wt_item': 'Z2',
                'wt_cmnt': "Please contact customer service for any questions"
            })
            
            # In a real system, this would insert the messages into the database
            logger.info(f"Inserted {len(messages)} print record lines for receive number {receive_no}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error inserting print record: {e}")
            return False
    
    def editor_appointment(self) -> bool:
        """
        Edit appointment details.
        
        Returns:
            True if saved, False if cancelled
        """
        sw = 1
        
        while sw:
            if sw == 1:
                print("\nF5:Previous F6:Current F7:Next Esc:Exit End:Finish")
                sw = self.edit_header()
            elif sw == 2:
                if self.chah_ind == AppointmentType.CONVERSION.value:
                    print("\nDel:Delete F5:Previous F6:Current F7:Next Esc:Buy End:Finish")
                else:
                    print("\nDel:Delete F5:Previous F6:Current F7:Next Esc:Remittance End:Finish")
                sw = self.edit_sw_sell()
            elif sw == 3:
                print("\nDel:Delete F5:Previous F6:Current F7:Next Esc:Confirm End:Finish")
                if self.chah_ind == AppointmentType.CONVERSION.value:
                    sw = self.edit_sw_buy()
                else:
                    sw = self.edit_remit_account()
            
            if not sw:
                return True
        
        return True
    
    def edit_header(self) -> int:
        """
        Edit appointment header.
        
        Returns:
            Next screen number or 0 to exit
        """
        sw = 2
        
        try:
            print("\nEdit Appointment Header:")
            
            # Get appointment type
            chah_ind = input(f"Appointment Type [1=Conversion, 2=Withdrawal] ({self.appointment_header.chah_ind}): ")
            if chah_ind:
                self.appointment_header.chah_ind = chah_ind
                
                # Update form based on appointment type
                if self.chah_ind != self.appointment_header.chah_ind:
                    self.chah_ind = self.appointment_header.chah_ind
                    self.set_input_form(False)
                    self.display_appointment()
                    self.display_sell(1)
                    if self.chah_ind == AppointmentType.CONVERSION.value:
                        self.display_buy(1)
                    else:
                        self.display_remit_data()
                
                # Validate appointment type against transaction code
                if self.appointment_header.chah_ind == AppointmentType.CONVERSION.value:
                    if self.display_info.po_chg_code != "73":
                        print("Policy does not have conversion transaction.")
                        return 1
                else:  # Withdrawal
                    if self.display_info.po_chg_code != "74":
                        print("Policy does not have withdrawal transaction.")
                        return 1
            
            # Get begin date
            bgn_date = input(f"Begin Date [YYY/MM/DD] ({self.appointment_header.bgn_date}): ")
            if bgn_date:
                if not self.check_date(bgn_date):
                    print("Invalid date format.")
                    return 1
                self.appointment_header.bgn_date = bgn_date
            
            # Get frequency
            chah_freq = input(f"Frequency [0=Once, 1=Monthly, 3=Quarterly, 6=Semi-annual, 12=Annual] ({self.appointment_header.chah_freq}): ")
            if chah_freq:
                try:
                    freq = int(chah_freq)
                    if freq not in [0, 1, 3, 6, 12]:
                        print("Invalid frequency. Must be 0, 1, 3, 6, or 12.")
                        return 1
                    self.appointment_header.chah_freq = freq
                except ValueError:
                    print("Invalid frequency. Must be a number.")
                    return 1
            
            # Validate one-time appointment date
            if self.appointment_header.chah_freq == 0 and self.appointment_header.bgn_date < self.today:
                print("Appointment date cannot be earlier than today for one-time appointments.")
                return 1
            
            # Update next transaction date
            self.get_next_tr_date()
            
            # Handle function keys
            key = input("Press F5 for Previous, F6 for Current, F7 for Next, or Enter to continue: ")
            if key == "F5":
                return 1
            elif key == "F6":
                return 2
            elif key == "F7":
                return 3
            
            return sw
            
        except KeyboardInterrupt:
            return 0
    
    def edit_sw_sell(self) -> int:
        """
        Edit sell investments.
        
        Returns:
            Next screen number or 0 to exit
        """
        sw = 3
        
        try:
            print("\nEdit Sell Investments:")
            print("Current sell records:")
            
            for i, sell in enumerate(self.sell_records):
                sell_type_desc = self.get_term_meaning("chah_sell_type", sell.chah_sell_type)
                print(f"{i+1}. Code: {sell.invs_code}, Type: {sell_type_desc}, Amount: {sell.invs_ad_amt}")
            
            while True:
                print("\nOptions: A)Add  E)Edit  D)Delete  C)Continue")
                choice = input("Select an option: ")
                
                if choice.upper() == "A":
                    # Add new sell record
                    new_sell = SellRecord()
                    
                    new_sell.invs_code = input("Investment Code: ")
                    if not new_sell.invs_code:
                        continue
                    
                    # Validate investment code
                    if not self.exam_sell_investment(len(self.sell_records) + 1):
                        print("Invalid investment code.")
                        continue
                    
                    # Check for duplicate appointment sell
                    if not self.check_duplicate_appointment_sell(len(self.sell_records) + 1):
                        print("Duplicate investment in another appointment conversion/withdrawal!")
                        continue
                    
                    new_sell.chah_sell_type = input("Sell Type [1=Amount, 2=All]: ")
                    if not new_sell.chah_sell_type or new_sell.chah_sell_type not in ["1", "2"]:
                        print("Invalid sell type.")
                        continue
                    
                    new_sell.chah_sell_type_desc = self.get_term_meaning("chah_sell_type", new_sell.chah_sell_type)
                    
                    if new_sell.chah_sell_type == SellType.AMOUNT.value:
                        try:
                            amount = float(input("Amount: "))
                            if amount <= 0:
                                print("Amount must be greater than 0.")
                                continue
                            
                            # Validate amount for TWD currency
                            if self.policy_info.currency == "TWD":
                                if amount != int(amount):
                                    print("TWD amount must be an integer.")
                                    continue
                            
                            new_sell.invs_ad_amt = amount
                        except ValueError:
                            print("Invalid amount.")
                            continue
                    else:
                        new_sell.invs_ad_amt = 0
                    
                    self.sell_records.append(new_sell)
                    print(f"Added sell record: {new_sell.invs_code}")
                
                elif choice.upper() == "E":
                    # Edit existing sell record
                    try:
                        index = int(input("Record number to edit: ")) - 1
                        if index < 0 or index >= len(self.sell_records):
                            print("Invalid record number.")
                            continue
                        
                        sell = self.sell_records[index]
                        
                        new_type = input(f"Sell Type [1=Amount, 2=All] ({sell.chah_sell_type}): ")
                        if new_type:
                            if new_type not in ["1", "2"]:
                                print("Invalid sell type.")
                                continue
                            sell.chah_sell_type = new_type
                            sell.chah_sell_type_desc = self.get_term_meaning("chah_sell_type", sell.chah_sell_type)
                        
                        if sell.chah_sell_type == SellType.AMOUNT.value:
                            try:
                                new_amount = input(f"Amount ({sell.invs_ad_amt}): ")
                                if new_amount:
                                    amount = float(new_amount)
                                    if amount <= 0:
                                        print("Amount must be greater than 0.")
                                        continue
                                    
                                    # Validate amount for TWD currency
                                    if self.policy_info.currency == "TWD":
                                        if amount != int(amount):
                                            print("TWD amount must be an integer.")
                                            continue
                                    
                                    sell.invs_ad_amt = amount
                            except ValueError:
                                print("Invalid amount.")
                                continue
                        else:
                            sell.invs_ad_amt = 0
                        
                        print(f"Updated sell record: {sell.invs_code}")
                    except ValueError:
                        print("Invalid record number.")
                        continue
                
                elif choice.upper() == "D":
                    # Delete sell record
                    try:
                        index = int(input("Record number to delete: ")) - 1
                        if index < 0 or index >= len(self.sell_records):
                            print("Invalid record number.")
                            continue
                        
                        code = self.sell_records[index].invs_code
                        del self.sell_records[index]
                        print(f"Deleted sell record: {code}")
                    except ValueError:
                        print("Invalid record number.")
                        continue
                
                elif choice.upper() == "C":
                    # Continue to next screen
                    break
                
                # Display updated records
                print("\nCurrent sell records:")
                for i, sell in enumerate(self.sell_records):
                    sell_type_desc = self.get_term_meaning("chah_sell_type", sell.chah_sell_type)
                    print(f"{i+1}. Code: {sell.invs_code}, Type: {sell_type_desc}, Amount: {sell.invs_ad_amt}")
            
            # Validate sell records
            self.check_sell_all()
            
            for i in range(len(self.sell_records)):
                if not self.check_duplicate_appointment_sell(i + 1):
                    print(f"Duplicate investment {self.sell_records[i].invs_code} in another appointment conversion/withdrawal!")
                    return 2
            
            if not self.sell_records:
                print("Please enter at least one sell record.")
                return 2
            
            if self.chah_ind == AppointmentType.WITHDRAWAL.value:
                self.sell_sum_amt = sum(sell.invs_ad_amt for sell in self.sell_records)
                if self.check_amt_ind and self.sell_sum_amt < self.plan_info.part_wd_amt_mini:
                    print(f"Total withdrawal amount is less than minimum ({self.plan_info.part_wd_amt_mini}).")
                    return 2
            
            # Handle function keys
            key = input("Press F5 for Previous, F6 for Current, F7 for Next, or Enter to continue: ")
            if key == "F5":
                return 1
            elif key == "F6":
                return 2
            elif key == "F7":
                return 3
            
            return sw
            
        except KeyboardInterrupt:
            return 0
    
    def edit_sw_buy(self) -> int:
        """
        Edit buy investments.
        
        Returns:
            Next screen number or 0 to exit
        """
        sw = 0
        
        try:
            print("\nEdit Buy Investments:")
            print("Current buy records:")
            
            for i, buy in enumerate(self.buy_records):
                print(f"{i+1}. Code: {buy.invs_code}, Percentage: {buy.invs_ad_perc}%")
            
            while True:
                print("\nOptions: A)Add  E)Edit  D)Delete  C)Continue")
                choice = input("Select an option: ")
                
                if choice.upper() == "A":
                    # Add new buy record
                    new_buy = BuyRecord()
                    
                    new_buy.invs_code = input("Investment Code: ")
                    if not new_buy.invs_code:
                        continue
                    
                    # Validate investment code
                    if not self.check_duplicate_invs(len(self.buy_records) + 1):
                        print("Duplicate investment code.")
                        continue
                    
                    if not self.check_duplicate_sell(len(self.buy_records) + 1):
                        print(f"Investment {new_buy.invs_code} is already in sell records.")
                        continue
                    
                    if not self.exam_buy_investment(len(self.buy_records) + 1):
                        continue
                    
                    try:
                        perc = float(input("Percentage: "))
                        if perc <= 0 or perc % 1 != 0 or perc < 5:
                            print("Percentage must be at least 5% and in whole numbers.")
                            continue
                        
                        new_buy.invs_ad_perc = perc
                    except ValueError:
                        print("Invalid percentage.")
                        continue
                    
                    self.buy_records.append(new_buy)
                    print(f"Added buy record: {new_buy.invs_code}")
                
                elif choice.upper() == "E":
                    # Edit existing buy record
                    try:
                        index = int(input("Record number to edit: ")) - 1
                        if index < 0 or index >= len(self.buy_records):
                            print("Invalid record number.")
                            continue
                        
                        buy = self.buy_records[index]
                        
                        try:
                            new_perc = input(f"Percentage ({buy.invs_ad_perc}): ")
                            if new_perc:
                                perc = float(new_perc)
                                if perc <= 0 or perc % 1 != 0 or perc < 5:
                                    print("Percentage must be at least 5% and in whole numbers.")
                                    continue
                                
                                buy.invs_ad_perc = perc
                        except ValueError:
                            print("Invalid percentage.")
                            continue
                        
                        print(f"Updated buy record: {buy.invs_code}")
                    except ValueError:
                        print("Invalid record number.")
                        continue
                
                elif choice.upper() == "D":
                    # Delete buy record
                    try:
                        index = int(input("Record number to delete: ")) - 1
                        if index < 0 or index >= len(self.buy_records):
                            print("Invalid record number.")
                            continue
                        
                        code = self.buy_records[index].invs_code
                        del self.buy_records[index]
                        print(f"Deleted buy record: {code}")
                    except ValueError:
                        print("Invalid record number.")
                        continue
                
                elif choice.upper() == "C":
                    # Continue to next screen
                    break
                
                # Display updated records
                print("\nCurrent buy records:")
                for i, buy in enumerate(self.buy_records):
                    print(f"{i+1}. Code: {buy.invs_code}, Percentage: {buy.invs_ad_perc}%")
            
            # Validate total percentage
            if not self.chk_and_show_ad_perc(1):
                print("Total percentage must equal 100%.")
                return 3
            
            # Check for duplicate investments between sell and buy
            for i in range(len(self.buy_records)):
                if not self.check_duplicate_sell(i + 1):
                    print(f"Investment {self.buy_records[i].invs_code} is already in sell records.")
                    return 3
            
            # Handle function keys
            key = input("Press F5 for Previous, F6 for Current, F7 for Next, or Enter to continue: ")
            if key == "F5":
                return 1
            elif key == "F6":
                return 2
            elif key == "F7":
                return 3
            
            return sw
            
        except KeyboardInterrupt:
            return 0
    
    def edit_remit_account(self) -> int:
        """
        Edit remittance account details.
        
        Returns:
            Next screen number or 0 to exit
        """
        sw = 0
        
        try:
            print("\nEdit Remittance Account:")
            
            # Get disbursement type
            disb_type = input(f"Disbursement Type [0=Bank Transfer, 1=Personal Account, 2=Policy Account] ({self.appointment_payment.chap_disb_type}): ")
            if disb_type:
                if disb_type not in ["0", "1", "2"]:
                    print("Invalid disbursement type.")
                    return 3
                
                self.appointment_payment.chap_disb_type = disb_type
                
                # Reset fields for account types
                if disb_type in ["1", "2"]:
                    self.appointment_payment.remit_bank = ""
                    self.appointment_payment.remit_branch = ""
                    self.appointment_payment.remit_account = ""
                    self.appointment_payment.payee = ""
                    self.appointment_payment.payee_e = ""
                    
                    # Validate account existence
                    if disb_type == "1":  # Personal account
                        if self.policy_info.currency == "TWD":
                            if not self.check_personal_account_twd():
                                print("No valid personal account found.")
                                return 3
                        else:
                            if not self.check_personal_account_foreign():
                                print("No valid personal account found.")
                                return 3
                    elif disb_type == "2":  # Policy account
                        if self.policy_info.currency == "TWD":
                            print("Invalid for TWD currency.")
                            return 3
                        else:
                            if not self.check_policy_account():
                                print("No valid policy account found.")
                                return 3
                
                # Set payee for bank transfer
                if disb_type == "0":
                    self.appointment_payment.payee = self.display_info.o1_name
            
            # Only ask for these fields for bank transfer
            if self.appointment_payment.chap_disb_type == "0":
                # Get bank code
                bank = input(f"Bank Code ({self.appointment_payment.remit_bank}): ")
                if bank:
                    self.appointment_payment.remit_bank = bank
                
                # Get branch code
                branch = input(f"Branch Code ({self.appointment_payment.remit_branch}): ")
                if branch:
                    self.appointment_payment.remit_branch = branch
                elif self.policy_info.currency != "TWD":
                    self.appointment_payment.remit_branch = "0000"
                
                # Validate bank
                bank_code = f"{self.appointment_payment.remit_bank}{self.appointment_payment.remit_branch}"
                bank_name = self.get_bank_name(bank_code)
                
                if not bank_name:
                    print("Invalid bank code.")
                    return 3
                
                if not self.check_bank_active(bank_code):
                    print("Bank is inactive.")
                    return 3
                
                print(f"Bank Name: {bank_name}")
                
                # Get account number
                account = input(f"Account Number ({self.appointment_payment.remit_account}): ")
                if account:
                    self.appointment_payment.remit_account = account
                
                # Get payee name
                payee = input(f"Payee Name ({self.appointment_payment.payee}): ")
                if payee:
                    self.appointment_payment.payee = payee
                
                # Get English payee name for foreign currency
                if self.policy_info.currency != "TWD":
                    payee_e = input(f"Payee Name (English) ({self.appointment_payment.payee_e}): ")
                    if payee_e:
                        self.appointment_payment.payee_e = payee_e
                        
                        # Validate English name
                        if not self.exam_chinese(self.appointment_payment.payee_e, len(self.appointment_payment.payee_e)):
                            print("English payee name cannot contain Chinese characters.")
                            return 3
                
                # Validate account
                if self.policy_info.currency == "TWD":
                    if not self.check_remit_acct(self.appointment_payment.remit_bank, 
                                               self.appointment_payment.remit_branch,
                                               self.appointment_payment.remit_account):
                        print("Invalid remittance account.")
                        return 3
                else:
                    # Get SWIFT code
                    swift_code = self.get_swift_code(bank_code)
                    if not swift_code:
                        print("Bank does not have a SWIFT code.")
                        return 3
                    
                    self.appointment_payment.swift_code = swift_code
                    self.appointment_payment.bank_name_e = self.get_bank_name_e(bank_code)
                    
                    # Check if English payee name is required
                    if self.is_payee_en_required(bank_code) and not self.appointment_payment.payee_e:
                        print("English payee name is required for this bank.")
                        return 3
                    
                    if not self.appointment_payment.remit_account:
                        print("Account number is required.")
                        return 3
                    
                    if not self.check_foreign_acct('1', self.appointment_payment.swift_code, 
                                                 self.appointment_payment.remit_account):
                        print("Invalid foreign account.")
                        return 3
            
            # Handle function keys
            key = input("Press F5 for Previous, F6 for Current, F7 for Next, or Enter to continue: ")
            if key == "F5":
                return 1
            elif key == "F6":
                return 2
            elif key == "F7":
                return 3
            
            return sw
            
        except KeyboardInterrupt:
            return 0
    
    def get_bank_name(self, bank_code: str) -> str:
        """
        Get bank name from bank code.
        
        Args:
            bank_code: The bank code
            
        Returns:
            The bank name
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT bank_name FROM bank WHERE bank_code = bank_code
        
        # Simulated response
        if bank_code:
            return f"Bank {bank_code}"
        return ""
    
    def loading_investment(self) -> None:
        """Load investment data."""
        # In a real system, this would query the database
        # Example query:
        # SELECT a.*, b.* FROM vpoiv a, vivdf b
        # WHERE a.invs_code = b.invs_code
        # AND a.policy_no = policy_no
        # AND a.invs_units != 0
        # ORDER BY a.invs_no
        
        # Simulated data
        pass
    
    def loading_chad(self) -> None:
        """Load appointment detail data."""
        # In a real system, this would query the database
        # Example query:
        # SELECT a.*, b.invs_sts_code, b.currency
        # FROM chad a, vivdf b
        # WHERE a.invs_code = b.invs_code
        # AND a.policy_no = policy_no
        # AND a.receive_no = receive_no
        # [AND a.chah_seq = chah_seq]
        # ORDER BY a.invs_ad_sub_ind desc, a.invs_code
        
        # Simulated data
        self.sell_records = []
        self.buy_records = []
        
        # Add sample data
        self.sell_records.append(SellRecord(
            invs_code="INV001",
            chah_sell_type="1",
            chah_sell_type_desc="Amount",
            invs_ad_amt=1000.0
        ))
        
        if self.chah_ind == AppointmentType.CONVERSION.value:
            self.buy_records.append(BuyRecord(
                invs_code="INV002",
                invs_ad_perc=100.0
            ))
        
        self.sell_sum_amt = sum(sell.invs_ad_amt for sell in self.sell_records)
        self.check_sell_all()
    
    def inserting_chad(self) -> None:
        """Insert appointment detail records."""
        # In a real system, this would insert data into the database
        
        # Insert sell records
        for sell in self.sell_records:
            # Example query:
            # INSERT INTO chad VALUES (
            #   chah_seq, policy_no, receive_no, "2", invs_code, 
            #   chah_sell_type, invs_ad_amt, 0
            # )
            logger.info(f"Inserted sell record: {sell.invs_code}")
        
        # Insert buy records
        for buy in self.buy_records:
            # Example query:
            # INSERT INTO chad VALUES (
            #   chah_seq, policy_no, receive_no, "1", invs_code, 
            #   "0", 0, invs_ad_perc
            # )
            logger.info(f"Inserted buy record: {buy.invs_code}")
    
    def deleting_chad(self) -> None:
        """Delete appointment detail records."""
        # In a real system, this would delete data from the database
        # Example query:
        # DELETE FROM chad WHERE chah_seq = chah_seq
        
        logger.info(f"Deleted detail records for chah_seq: {self.appointment_header.chah_seq}")
    
    def inserting_chah(self) -> None:
        """Insert appointment header record."""
        # In a real system, this would insert data into the database
        # Example query:
        # INSERT INTO chah VALUES (...)
        
        # Simulate getting the sequence number
        self.appointment_header.chah_seq = 12345
        
        logger.info(f"Inserted header record: {self.appointment_header.chah_seq}")
        
        # Insert payment record for withdrawal
        if self.chah_ind == AppointmentType.WITHDRAWAL.value:
            self.appointment_payment.chah_seq = self.appointment_header.chah_seq
            self.appointment_payment.policy_no = self.appointment_header.policy_no
            self.appointment_payment.receive_no = self.appointment_header.receive_no
            
            # Example query:
            # INSERT INTO chap VALUES (...)
            
            logger.info(f"Inserted payment record for chah_seq: {self.appointment_header.chah_seq}")
    
    def updating_chah(self) -> None:
        """Update appointment header record."""
        # In a real system, this would update data in the database
        # Example query:
        # UPDATE chah SET ... WHERE chah_seq = chah_seq
        
        logger.info(f"Updated header record: {self.appointment_header.chah_seq}")
        
        # Delete and reinsert payment record for withdrawal
        # Example query:
        # DELETE FROM chap WHERE chah_seq = chah_seq
        
        if self.chah_ind == AppointmentType.WITHDRAWAL.value:
            # Example query:
            # INSERT INTO chap VALUES (...)
            
            logger.info(f"Updated payment record for chah_seq: {self.appointment_header.chah_seq}")
    
    def loading_data(self) -> None:
        """Load all related data."""
        if self.appointment_header.chah_ind:
            self.chah_ind = self.appointment_header.chah_ind
        
        self.set_input_form(False)
        
        # Load policy data
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM polf WHERE policy_no = policy_no
        
        # Simulated data
        self.policy_info = PolicyInfo(
            policy_no=self.appointment_header.policy_no,
            po_sts_code="42",
            currency="TWD",
            basic_plan_code="PLAN001",
            insurance_type="V",
            basic_rate_scale="1"
        )
        
        # Load client data
        # In a real system, this would query the database
        # Example queries:
        # SELECT a.client_id, b.names FROM pocl a, clnt b
        # WHERE policy_no = policy_no AND client_ident = "O1" AND a.client_id = b.client_id
        # 
        # SELECT a.client_id, b.names FROM pocl a, clnt b
        # WHERE policy_no = policy_no AND client_ident = "I1" AND a.client_id = b.client_id
        
        # Simulated data
        self.client_info = ClientInfo(
            owner_id="O12345",
            o1_name="John Doe",
            client_id="I12345",
            names="Jane Doe"
        )
        
        self.display_info.o1_name = self.client_info.o1_name
        self.display_info.names = self.client_info.names
        self.display_info.owner_id = self.client_info.owner_id
        self.display_info.client_id = self.client_info.client_id
        
        # Get currency description
        self.display_info.c_desc = self.get_currency_description(self.policy_info.currency)
        
        # Load plan data
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM pldf
        # WHERE plan_code = basic_plan_code AND rate_scale = basic_rate_scale
        
        # Simulated data
        self.plan_info = PlanInfo(
            part_wd_amt_mini=1000.0,
            invs_avail_type="2",
            iv_ass_array="111",
            ivchg_array="111"
        )
        
        # Load payment data for withdrawal
        if self.appointment_header.chah_ind == AppointmentType.WITHDRAWAL.value:
            self.loading_chap()
        
        # Load detail data
        self.loading_chad()
    
    def loading_chap(self) -> None:
        """Load payment data."""
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM chap
        # WHERE policy_no = policy_no AND receive_no = receive_no AND chah_seq = chah_seq
        
        # Simulated data
        self.appointment_payment = AppointmentPayment(
            chah_seq=self.appointment_header.chah_seq,
            policy_no=self.appointment_header.policy_no,
            receive_no=self.appointment_header.receive_no,
            chap_disb_type="0",
            remit_bank="123",
            remit_branch="456",
            remit_account="78901234",
            payee=self.display_info.o1_name,
            payee_e="",
            payee_id=self.display_info.owner_id
        )
    
    def saving_cancel(self) -> None:
        """Save cancellation."""
        try:
            # In a real system, this would update data in the database
            # Example query:
            # UPDATE chah SET active_ind = '1' WHERE chah_seq = chah_seq
            
            logger.info(f"Cancelled appointment: {self.appointment_header.chah_seq}")
        except Exception as e:
            logger.error(f"Error cancelling appointment: {e}")
            raise
    
    def saving_modify(self) -> None:
        """Save modifications."""
        try:
            # In a real system, this would update data in the database
            # Example query:
            # UPDATE chah SET ... WHERE policy_no = policy_no AND receive_no = receive_no AND chah_seq = chah_seq
            
            self.deleting_chad()
            self.inserting_chad()
            
            logger.info(f"Modified appointment: {self.appointment_header.chah_seq}")
        except Exception as e:
            logger.error(f"Error modifying appointment: {e}")
            raise
    
    def saving_approval(self) -> None:
        """Save approval."""
        try:
            # Set active status
            self.appointment_header.active_ind = ActiveStatus.ACTIVE.value
            
            # Update next transaction date
            self.get_next_tr_date()
            
            # In a real system, this would update data in the database
            # Example query:
            # UPDATE chah SET ... WHERE policy_no = policy_no AND receive_no = receive_no AND chah_seq = chah_seq
            
            logger.info(f"Approved appointment: {self.appointment_header.chah_seq}")
        except Exception as e:
            logger.error(f"Error approving appointment: {e}")
            raise
    
    def check_invest_condition(self) -> bool:
        """
        Check if the policy meets investment conditions.
        
        Returns:
            True if conditions are met, False otherwise
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM chah WHERE policy_no = policy_no AND receive_no = receive_no
        
        # Check if appointment exists
        # Simulated logic
        if self.process_ind == ProcessType.ADD.value:
            self.is_new = True
            return True
        else:
            # Appointment exists
            self.is_new = False
            
            # Check active status
            if self.appointment_header.active_ind != ActiveStatus.PENDING.value:
                if self.appointment_header.active_ind == ActiveStatus.ACTIVE.value:
                    print("This appointment has already been approved!")
                elif self.appointment_header.active_ind == ActiveStatus.CANCELLED.value:
                    print("This appointment has already been cancelled!")
                elif self.appointment_header.active_ind == ActiveStatus.EXPIRED.value:
                    print("This appointment has already expired!")
                return False
            
            return True
    
    def check_policy_condition(self) -> bool:
        """
        Check if the policy meets conditions for investment appointment.
        
        Returns:
            True if conditions are met, False otherwise
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM polf WHERE policy_no = policy_no
        
        # Check policy status
        if self.policy_info.po_sts_code not in ["42", "44", "47"]:
            print("Policy status must be 42, 44, or 47.")
            return False
        
        # Check insurance type
        if self.policy_info.insurance_type not in ["V", "N", "G"]:
            print("Policy is not an investment policy.")
            return False
        
        # Check if plan allows investment appointment
        if self.plan_info.iv_ass_array[2] == "0" or self.plan_info.iv_ass_array[0] == "0":
            print("Policy plan does not allow investment appointment.")
            return False
        
        if self.plan_info.ivchg_array[2] == "0" or self.plan_info.ivchg_array[0] == "0":
            print("Policy plan does not allow investment conversion or withdrawal.")
            return False
        
        # Set currency description
        self.display_info.c_desc = self.get_currency_description(self.policy_info.currency)
        
        return True
    
    def initialization(self, reset: bool) -> bool:
        """
        Initialize appointment data.
        
        Args:
            reset: Whether to reset all data
            
        Returns:
            True if successful, False otherwise
        """
        if reset or self.is_new:
            self.appointment_header.chah_seq = 0
            self.appointment_header.currency = self.policy_info.currency
            self.appointment_header.active_ind = ActiveStatus.PENDING.value
            self.appointment_payment = AppointmentPayment()
            self.sell_records = []
            self.buy_records = []
        
        self.display_appointment()
        self.loading_investment()
        
        self.appointment_header.process_date = self.today
        self.appointment_header.process_user = self.user_id
        
        self.sell_sum_amt = 0.0
        
        return True
    
    def exam_sell_investment(self, index: int) -> bool:
        """
        Validate sell investment.
        
        Args:
            index: The index of the investment to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check for duplicate investments
        for i in range(len(self.sell_records)):
            if i != index - 1 and self.sell_records[i].invs_code == self.sell_records[index - 1].invs_code:
                print("Duplicate investment code.")
                return False
        
        # Check if investment exists and is available for conversion
        if not self.check_investment_exists(self.appointment_header.policy_no, self.sell_records[index - 1].invs_code):
            print("Investment does not exist or is not available for conversion.")
            return False
        
        return True
    
    def exam_buy_investment(self, index: int) -> bool:
        """
        Validate buy investment.
        
        Args:
            index: The index of the investment to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check for duplicate investments
        if not self.check_duplicate_invs(index):
            print("Duplicate investment code.")
            return False
        
        # Check if investment is also in sell records
        if not self.check_duplicate_sell(index):
            print("Investment is already in sell records.")
            return False
        
        # Check if investment exists and is available for conversion
        if not self.check_investment_exists(self.appointment_header.policy_no, self.buy_records[index - 1].invs_code):
            print("Investment does not exist or is not available for conversion.")
            return False
        
        # Check if investment is shutting down
        if self.is_investment_shutting(self.buy_records[index - 1].invs_code, self.display_info.receive_date):
            print("Investment is shutting down and cannot be purchased.")
            return False
        
        # Check risk level
        if not self.check_investment_risk(self.display_info.owner_id, self.buy_records[index - 1].invs_code):
            print("Investment risk level exceeds owner's risk tolerance.")
            return False
        
        return True
    
    def check_duplicate_invs(self, index: int) -> bool:
        """
        Check for duplicate investments in buy records.
        
        Args:
            index: The index of the investment to check
            
        Returns:
            True if no duplicates, False otherwise
        """
        for i in range(len(self.buy_records)):
            if i != index - 1 and self.buy_records[i].invs_code == self.buy_records[index - 1].invs_code:
                return False
        return True
    
    def check_duplicate_sell(self, index: int) -> bool:
        """
        Check if buy investment is also in sell records.
        
        Args:
            index: The index of the buy investment to check
            
        Returns:
            True if not in sell records, False otherwise
        """
        for sell in self.sell_records:
            if self.buy_records[index - 1].invs_code == sell.invs_code:
                return False
        return True
    
    def check_investment_exists(self, policy_no: str, invs_code: str) -> bool:
        """
        Check if investment exists and is available for conversion.
        
        Args:
            policy_no: The policy number
            invs_code: The investment code
            
        Returns:
            True if exists and available, False otherwise
        """
        # In a real system, this would query the database
        # Example function call:
        # ar904_check_invs(policy_no, invs_code)
        
        # Simulated response
        return True
    
    def is_investment_shutting(self, invs_code: str, receive_date: str) -> bool:
        """
        Check if investment is shutting down.
        
        Args:
            invs_code: The investment code
            receive_date: The receive date
            
        Returns:
            True if shutting down, False otherwise
        """
        # In a real system, this would check if the investment is shutting down
        # Example check:
        # ar904_shutting IS NOT NULL AND ar904_shutting != " " AND receive_date > ar904_shutting
        
        # Simulated response
        return False
    
    def check_investment_risk(self, client_id: str, invs_code: str) -> bool:
        """
        Check if investment risk level is acceptable for the client.
        
        Args:
            client_id: The client ID
            invs_code: The investment code
            
        Returns:
            True if risk is acceptable, False otherwise
        """
        # In a real system, this would check the client's risk tolerance
        # Example function call:
        # iv993p_risk_id(client_id)
        
        # Simulated response
        return True
    
    def chk_and_show_ad_perc(self, start_index: int) -> bool:
        """
        Check if buy percentages sum to 100%.
        
        Args:
            start_index: The starting index
            
        Returns:
            True if sum is 100%, False otherwise
        """
        total = sum(buy.invs_ad_perc for buy in self.buy_records)
        return total == 100.0
    
    def check_sell_all(self) -> None:
        """Check if any sell record is 'sell all'."""
        self.check_amt_ind = True
        
        for sell in self.sell_records:
            if sell.chah_sell_type == SellType.ALL.value:
                self.check_amt_ind = False
                break
    
    def get_term_meaning(self, term_type: str, term_code: str) -> str:
        """
        Get the meaning of a term code.
        
        Args:
            term_type: The type of term
            term_code: The term code
            
        Returns:
            The term meaning
        """
        # In a real system, this would query the database
        
        if term_type == "chah_sell_type":
            if term_code == "1":
                return "Amount"
            elif term_code == "2":
                return "All"
        
        return ""
    
    def get_currency_description(self, currency: str) -> str:
        """
        Get the description of a currency.
        
        Args:
            currency: The currency code
            
        Returns:
            The currency description
        """
        # In a real system, this would query the database
        # Example function call:
        # ar901_get_currency(currency)
        
        if currency == "TWD":
            return "New Taiwan Dollar"
        elif currency == "USD":
            return "US Dollar"
        elif currency == "CNY":
            return "Chinese Yuan"
        
        return ""
    
    def check_date(self, date_str: str) -> bool:
        """
        Check if a date string is valid.
        
        Args:
            date_str: The date string to check
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Format: YYY/MM/DD (Taiwan calendar format)
            parts = date_str.split('/')
            if len(parts) != 3:
                return False
            
            year = int(parts[0]) + 1911  # Convert to Gregorian calendar
            month = int(parts[1])
            day = int(parts[2])
            
            datetime.date(year, month, day)
            return True
        except ValueError:
            return False
    
    def get_next_tr_date(self) -> None:
        """Calculate the next transaction date."""
        if not self.appointment_header.bgn_date:
            return
        
        # Start with begin date
        self.appointment_header.auto_tr_date = self.appointment_header.bgn_date
        
        # If frequency is not one-time, calculate next date after process date
        if self.appointment_header.chah_freq > 0:
            i = 0
            while self.appointment_header.auto_tr_date < self.appointment_header.process_date and i < 10:
                self.appointment_header.auto_tr_date = self.add_month(
                    self.appointment_header.auto_tr_date, 
                    self.appointment_header.chah_freq
                )
                i += 1
    
    def add_month(self, date_str: str, months: int) -> str:
        """
        Add months to a date string.
        
        Args:
            date_str: The date string
            months: The number of months to add
            
        Returns:
            The new date string
        """
        # Format: YYY/MM/DD (Taiwan calendar format)
        parts = date_str.split('/')
        year = int(parts[0]) + 1911  # Convert to Gregorian calendar
        month = int(parts[1])
        day = int(parts[2])
        
        # Calculate new date
        month += months
        year += (month - 1) // 12
        month = ((month - 1) % 12) + 1
        
        # Handle day overflow (e.g., Jan 31 + 1 month = Feb 28/29)
        last_day = self.get_last_day_of_month(year, month)
        if day > last_day:
            day = last_day
        
        # Convert back to Taiwan calendar format
        taiwan_year = year - 1911
        return f"{taiwan_year:03d}/{month:02d}/{day:02d}"
    
    def get_last_day_of_month(self, year: int, month: int) -> int:
        """
        Get the last day of a month.
        
        Args:
            year: The year
            month: The month
            
        Returns:
            The last day of the month
        """
        if month == 12:
            next_month = datetime.date(year + 1, 1, 1)
        else:
            next_month = datetime.date(year, month + 1, 1)
        
        last_day = next_month - datetime.timedelta(days=1)
        return last_day.day
    
    def check_duplicate_appointment_sell(self, index: int) -> bool:
        """
        Check if there's a duplicate investment in another appointment.
        
        Args:
            index: The index of the sell record to check (0 to check all)
            
        Returns:
            True if no duplicates, False otherwise
        """
        # In a real system, this would query the database
        
        if index < 0:
            return False
        
        # Determine which records to check
        if index == 0:
            start_idx = 0
            end_idx = len(self.sell_records) - 1
        else:
            start_idx = index - 1
            end_idx = index - 1
        
        # Get month and day of begin date
        if not self.appointment_header.bgn_date:
            return True
        
        bgn_date_month_day = self.appointment_header.bgn_date[4:9]  # MM/DD
        
        # Check each record
        for i in range(start_idx, end_idx + 1):
            # In a real system, this would query the database
            # Example query:
            # SELECT COUNT(*) FROM chah a, chad b
            # WHERE a.policy_no = policy_no
            # AND a.chah_seq = b.chah_seq
            # AND a.bgn_date[5,9] = bgn_date_month_day
            # AND a.receive_no <> receive_no
            # AND b.invs_ad_sub_ind = "2"
            # AND b.invs_code = sell_records[i].invs_code
            # AND a.active_ind = "0"
            
            # Simulated response
            exists = False
            
            if exists:
                return False
        
        return True
    
    def check_appointment_started(self) -> bool:
        """
        Check if the appointment has already started processing.
        
        Returns:
            True if started, False otherwise
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT COUNT(*) FROM chah a, chlh b
        # WHERE a.chah_seq = b.chah_seq
        # AND a.chah_seq = chah_seq
        
        # Simulated response
        return False
    
    def check_owner(self) -> bool:
        """
        Check if the current user is the owner of the transaction.
        
        Returns:
            True if owner, False otherwise
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM bpqi WHERE receive_no = receive_no
        
        # Simulated response
        return True
    
    def check_authorization(self, receive_no: str, auth_code: str, level: int) -> bool:
        """
        Check if the user has authorization for the operation.
        
        Args:
            receive_no: The receive number
            auth_code: The authorization code
            level: The authorization level
            
        Returns:
            True if authorized, False otherwise
        """
        # In a real system, this would check authorization
        # Example function call:
        # ps996_auth_check(receive_no, auth_code, level)
        
        # Simulated response
        return True
    
    def check_personal_account_twd(self) -> bool:
        """
        Check if the client has a valid TWD personal account.
        
        Returns:
            True if valid account exists, False otherwise
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT COUNT(*) FROM psra
        # WHERE client_id = owner_id AND psra_sts_code = '0'
        
        # Simulated response
        return True
    
    def check_personal_account_foreign(self) -> bool:
        """
        Check if the client has a valid foreign currency personal account.
        
        Returns:
            True if valid account exists, False otherwise
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT COUNT(*) FROM psrf
        # WHERE client_id = owner_id AND psrf_sts_code = '0'
        
        # Simulated response
        return True
    
    def check_policy_account(self) -> bool:
        """
        Check if the policy has a valid account.
        
        Returns:
            True if valid account exists, False otherwise
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT COUNT(*) FROM pofb
        # WHERE client_id = owner_id AND policy_no = policy_no
        
        # Simulated response
        return True
    
    def check_bank_active(self, bank_code: str) -> bool:
        """
        Check if a bank is active.
        
        Args:
            bank_code: The bank code
            
        Returns:
            True if active, False otherwise
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT * FROM bank WHERE bank_code = bank_code AND bank_use_ind = 'N'
        
        # Simulated response
        return True
    
    def check_remit_acct(self, bank: str, branch: str, account: str) -> bool:
        """
        Check if a remittance account is valid.
        
        Args:
            bank: The bank code
            branch: The branch code
            account: The account number
            
        Returns:
            True if valid, False otherwise
        """
        # In a real system, this would validate the account
        # Example function call:
        # chkRemitAcct(bank, branch, account)
        
        # Simulated response
        return True
    
    def get_swift_code(self, bank_code: str) -> str:
        """
        Get the SWIFT code for a bank.
        
        Args:
            bank_code: The bank code
            
        Returns:
            The SWIFT code
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT swift_code FROM bksw
        # WHERE bank_code = bank_code AND bank_use_ind = "Y"
        
        # Simulated response
        return "SWIFTCODE"
    
    def get_bank_name_e(self, bank_code: str) -> str:
        """
        Get the English name of a bank.
        
        Args:
            bank_code: The bank code
            
        Returns:
            The English bank name
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT bank_name_e FROM bksw
        # WHERE bank_code = bank_code AND bank_use_ind = "Y"
        
        # Simulated response
        return "Bank Name (English)"
    
    def is_payee_en_required(self, bank_code: str) -> bool:
        """
        Check if English payee name is required for a bank.
        
        Args:
            bank_code: The bank code
            
        Returns:
            True if required, False otherwise
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT payee_en_ind FROM bksw
        # WHERE bank_code = bank_code AND bank_use_ind = "Y"
        
        # Simulated response
        return True
    
    def check_foreign_acct(self, acct_type: str, swift_code: str, account: str) -> bool:
        """
        Check if a foreign account is valid.
        
        Args:
            acct_type: The account type
            swift_code: The SWIFT code
            account: The account number
            
        Returns:
            True if valid, False otherwise
        """
        # In a real system, this would validate the account
        # Example function call:
        # chk_foreignacct(acct_type, swift_code, account)
        
        # Simulated response
        return True
    
    def exam_chinese(self, text: str, length: int) -> bool:
        """
        Check if text contains Chinese characters.
        
        Args:
            text: The text to check
            length: The length of the text
            
        Returns:
            True if no Chinese characters, False otherwise
        """
        # In a real system, this would check for Chinese characters
        
        # Simple check for demonstration
        for char in text:
            if ord(char) > 127:
                return False
        
        return True
    
    def get_investment_title(self, invs_code: str) -> str:
        """
        Get the title of an investment.
        
        Args:
            invs_code: The investment code
            
        Returns:
            The investment title
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT invs_title FROM vivdf WHERE invs_code = invs_code
        
        # Simulated response
        return "Investment Title"
    
    def query_psrd(self, receive_no: str) -> None:
        """
        Display print record data.
        
        Args:
            receive_no: The receive number
        """
        # In a real system, this would query the database
        # Example query:
        # SELECT wt_item, wt_cmnt, rece_seq FROM psrd
        # WHERE receive_no = receive_no ORDER BY 3
        
        print("\n=== Print Record ===")
        print("Policy Number:", self.appointment_header.policy_no)
        print("Receive Number:", receive_no)
        print("Process Date:", self.appointment_header.process_date)
        
        # Simulated data
        print("Line 1: Policy information")
        print("Line 2: Process date information")
        print("Line 3: Appointment details")
        print("Line 4: Investment details")
        print("Line 5: Thank you message")
    
    def insert_pble(self, policy_no: str, receive_no: str, doc_type: str) -> bool:
        """
        Insert policy letter record.
        
        Args:
            policy_no: The policy number
            receive_no: The receive number
            doc_type: The document type
            
        Returns:
            True if successful, False otherwise
        """
        # In a real system, this would insert data into the database
        
        logger.info(f"Inserted policy letter record for policy {policy_no}, receive {receive_no}")
        return True
    
    def print_po_only(self, policy_no: str, receive_no: str, print_type: str) -> bool:
        """
        Print policy documents.
        
        Args:
            policy_no: The policy number
            receive_no: The receive number
            print_type: The print type
            
        Returns:
            True if successful, False otherwise
        """
        # In a real system, this would print documents
        
        logger.info(f"Printed policy documents type {print_type} for policy {policy_no}, receive {receive_no}")
        return True
    
    def update_transaction_status(self, receive_no: str, status: str) -> None:
        """
        Update transaction status.
        
        Args:
            receive_no: The receive number
            status: The new status
        """
        # In a real system, this would update data in the database
        # Example function call:
        # ap905_update_sts(receive_no, status)
        
        logger.info(f"Updated transaction status to {status} for receive {receive_no}")


if __name__ == "__main__":
    system = InvestmentAppointmentSystem()
    system.main()
