
import xml.etree.ElementTree as ET
from datetime import date
import os


class JobApplicationTracker:

    def __init__(self):
        self.file_name = "job_applications.xml"
        self.tree = None
        self.root = None
        self.load_applications()

    def load_applications(self):
        if os.path.exists(self.file_name):
            try:
                self.tree = ET.parse(self.file_name)
                self.root = self.tree.getroot()
            except ET.ParseError:
                print("XML file is invalid. Creating a new file.")
                self.root = ET.Element("jobApplications")
                self.tree = ET.ElementTree(self.root)
        else:
            self.root = ET.Element("jobApplications")
            self.tree = ET.ElementTree(self.root)

    def save_applications(self):
        self.tree = ET.ElementTree(self.root)
        self.tree.write(
            self.file_name,
            encoding="utf-8",
            xml_declaration=True
        )
        print("Applications saved successfully!")

    def display_applications(self):
        applications = self.root.findall("application")

        if not applications:
            print("\nNo job applications found.")
            return

        print("\n========== JOB APPLICATIONS ==========")

        for index, application in enumerate(applications, start=1):
            first_name = application.findtext("applicant/name/first", "")
            last_name = application.findtext("applicant/name/last", "")
            title = application.findtext("position/title", "")
            company = application.findtext("position/company", "")
            location = application.findtext("position/location", "")
            status = application.findtext("applicationStatus/status", "")
            submitted_date = application.findtext("applicationStatus/date", "")

            print(f"\nApplication ID: {index}")
            print(f"Applicant: {first_name} {last_name}")
            print(f"Position: {title}")
            print(f"Company: {company}")
            print(f"Location: {location}")
            print(f"Status: {status}")
            print(f"Date Applied: {submitted_date}")

        print("\n======================================")

    def add_application(self):
        print("\n========== ADD APPLICATION ==========")

        first_name = input("Enter first name: ").strip()
        last_name = input("Enter last name: ").strip()
        email = input("Enter email address: ").strip()
        phone = input("Enter phone number: ").strip()

        title = input("Enter job position: ").strip()
        company = input("Enter company name: ").strip()
        location = input("Enter job location: ").strip()

        if not all([first_name, last_name, email, phone, title, company, location]):
            print("All fields are required. Please try again.")
            return

        if "@" not in email or "." not in email:
            print("Please enter a valid email address.")
            return

        status = "Applied"
        submitted_date = str(date.today())

        application = ET.SubElement(self.root, "application")

        applicant = ET.SubElement(application, "applicant")

        name = ET.SubElement(applicant, "name")
        ET.SubElement(name, "first").text = first_name
        ET.SubElement(name, "last").text = last_name

        contact = ET.SubElement(applicant, "contact")
        ET.SubElement(contact, "email").text = email
        ET.SubElement(contact, "phone").text = phone

        position = ET.SubElement(application, "position")
        ET.SubElement(position, "title").text = title
        ET.SubElement(position, "company").text = company
        ET.SubElement(position, "location").text = location

        application_status = ET.SubElement(application, "applicationStatus")
        ET.SubElement(application_status, "status").text = status
        ET.SubElement(application_status, "date").text = submitted_date

        self.save_applications()
        print("Job application added successfully!")

    def search_application(self):
        company_name = input("\nEnter company name to search: ").strip().lower()

        if not company_name:
            print("Please enter a company name.")
            return

        found = False

        for application in self.root.findall("application"):
            company = application.findtext("position/company", "")

            if company_name in company.lower():
                title = application.findtext("position/title", "")
                status = application.findtext("applicationStatus/status", "")

                print("\nApplication Found!")
                print(f"Company: {company}")
                print(f"Position: {title}")
                print(f"Status: {status}")

                found = True

        if not found:
            print("No matching application found.")

    def update_status(self):
        applications = self.root.findall("application")

        if not applications:
            print("\nNo applications available to update.")
            return

        self.display_applications()

        try:
            application_id = int(input("\nEnter Application ID: "))

            if application_id < 1 or application_id > len(applications):
                print("Invalid Application ID.")
                return

            print("\nAvailable Status:")
            print("1. Applied")
            print("2. Interview")
            print("3. Selected")
            print("4. Rejected")

            status_choice = input("Choose new status: ").strip()

            statuses = {
                "1": "Applied",
                "2": "Interview",
                "3": "Selected",
                "4": "Rejected"
            }

            if status_choice not in statuses:
                print("Invalid status choice.")
                return

            application = applications[application_id - 1]
            status_element = application.find("applicationStatus/status")
            status_element.text = statuses[status_choice]

            self.save_applications()
            print("Application status updated successfully!")

        except ValueError:
            print("Please enter a valid numeric ID.")

    def delete_application(self):
        applications = self.root.findall("application")

        if not applications:
            print("\nNo applications available to delete.")
            return

        self.display_applications()

        try:
            application_id = int(input("\nEnter Application ID to delete: "))

            if application_id < 1 or application_id > len(applications):
                print("Invalid Application ID.")
                return

            application = applications[application_id - 1]

            confirm = input("Are you sure you want to delete? (yes/no): ").strip().lower()

            if confirm == "yes":
                self.root.remove(application)
                self.save_applications()
                print("Application deleted successfully!")
            else:
                print("Delete operation cancelled.")

        except ValueError:
            print("Please enter a valid numeric ID.")

    def run(self):
        while True:
            print("\n========== JOB APPLICATION TRACKER ==========")
            print("1. View Applications")
            print("2. Add Application")
            print("3. Search Application")
            print("4. Update Application Status")
            print("5. Delete Application")
            print("6. Save and Exit")

            choice = input("\nEnter your choice (1-6): ").strip()

            if choice == "1":
                self.display_applications()

            elif choice == "2":
                self.add_application()

            elif choice == "3":
                self.search_application()

            elif choice == "4":
                self.update_status()

            elif choice == "5":
                self.delete_application()

            elif choice == "6":
                self.save_applications()
                print("Thank you for using Job Application Tracker!")
                break

            else:
                print("Invalid choice. Please select between 1 and 6.")


if __name__ == "__main__":
    app = JobApplicationTracker()
    app.run()
