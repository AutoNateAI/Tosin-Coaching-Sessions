import csv
import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd
from rich.console import Console
from rich.table import Table

class InternshipSearchTracker:
    """A tool for tracking and analyzing internship search activities and results."""
    
    def __init__(self, data_dir="data"):
        """Initialize the tracker with data directory."""
        self.data_dir = data_dir
        self.console = Console()
        
        # Ensure data directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        # Initialize or load tracking files
        self.company_file = os.path.join(data_dir, "company_contacts.csv")
        self.engagement_file = os.path.join(data_dir, "engagement_tracker.csv")
        self.query_file = os.path.join(data_dir, "search_queries.csv")
        
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize tracking files if they don't exist."""
        # Company contacts file
        if not os.path.exists(self.company_file):
            with open(self.company_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Company Name",
                    "Industry",
                    "Company Size",
                    "Job Posting URL",
                    "Technologies",
                    "Engineering Manager Name",
                    "Engineering Manager LinkedIn",
                    "Recruiter Name",
                    "Recruiter LinkedIn",
                    "Team Lead Name",
                    "Team Lead LinkedIn",
                    "Mutual Connections",
                    "Contact Status",
                    "Last Contact Date",
                    "Notes"
                ])
        
        # Engagement tracker file
        if not os.path.exists(self.engagement_file):
            with open(self.engagement_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Contact Name",
                    "Company",
                    "Position",
                    "Platform",
                    "Engagement Type",
                    "Date",
                    "Content Sent",
                    "Response Received",
                    "Response Time (hours)",
                    "Next Action",
                    "Next Action Date",
                    "Status",
                    "Notes"
                ])
        
        # Search queries file
        if not os.path.exists(self.query_file):
            with open(self.query_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Platform", "Query", "Date Added", "Results Count", "Effectiveness Rating"])
    
    def add_company(self, company_data):
        """Add a new company to the tracking system.
        
        Args:
            company_data (dict): Dictionary containing company information
        """
        required_fields = ["Company Name", "Industry", "Technologies"]
        for field in required_fields:
            if field not in company_data:
                self.console.print(f"[bold red]Error:[/bold red] Missing required field: {field}")
                return False
        
        # Add current date if not provided
        if "Last Contact Date" not in company_data:
            company_data["Last Contact Date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Read existing data to check for duplicates
        companies = []
        try:
            with open(self.company_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                companies = list(reader)
        except Exception as e:
            self.console.print(f"[bold yellow]Warning:[/bold yellow] {str(e)}")
        
        # Check for duplicates
        for company in companies:
            if company.get("Company Name") == company_data["Company Name"]:
                self.console.print(f"[bold yellow]Warning:[/bold yellow] Company {company_data['Company Name']} already exists. Use update_company instead.")
                return False
        
        # Write to file
        with open(self.company_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(company_data.keys()))
            writer.writerow(company_data)
        
        self.console.print(f"[bold green]Success:[/bold green] Added {company_data['Company Name']} to tracking system")
        return True
    
    def add_engagement(self, engagement_data):
        """Add a new engagement activity to the tracking system.
        
        Args:
            engagement_data (dict): Dictionary containing engagement information
        """
        required_fields = ["Contact Name", "Company", "Platform", "Engagement Type"]
        for field in required_fields:
            if field not in engagement_data:
                self.console.print(f"[bold red]Error:[/bold red] Missing required field: {field}")
                return False
        
        # Add current date if not provided
        if "Date" not in engagement_data:
            engagement_data["Date"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Write to file
        with open(self.engagement_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(engagement_data.keys()))
            writer.writerow(engagement_data)
        
        self.console.print(f"[bold green]Success:[/bold green] Added engagement with {engagement_data['Contact Name']} to tracking system")
        return True
    
    def add_search_query(self, query_data):
        """Add a new search query to the tracking system.
        
        Args:
            query_data (dict): Dictionary containing query information
        """
        required_fields = ["Platform", "Query"]
        for field in required_fields:
            if field not in query_data:
                self.console.print(f"[bold red]Error:[/bold red] Missing required field: {field}")
                return False
        
        # Add current date if not provided
        if "Date Added" not in query_data:
            query_data["Date Added"] = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Write to file
        with open(self.query_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(query_data.keys()))
            writer.writerow(query_data)
        
        self.console.print(f"[bold green]Success:[/bold green] Added search query for {query_data['Platform']} to tracking system")
        return True
    
    def update_company_status(self, company_name, new_status, notes=None):
        """Update the status of a company in the tracking system.
        
        Args:
            company_name (str): Name of the company to update
            new_status (str): New status value
            notes (str, optional): Additional notes to add
        """
        companies = []
        try:
            with open(self.company_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                companies = list(reader)
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
            return False
        
        # Find and update the company
        found = False
        for company in companies:
            if company["Company Name"] == company_name:
                company["Contact Status"] = new_status
                company["Last Contact Date"] = datetime.datetime.now().strftime("%Y-%m-%d")
                if notes:
                    company["Notes"] = notes
                found = True
                break
        
        if not found:
            self.console.print(f"[bold yellow]Warning:[/bold yellow] Company {company_name} not found in tracking system")
            return False
        
        # Write updated data back to file
        with open(self.company_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(companies)
        
        self.console.print(f"[bold green]Success:[/bold green] Updated status for {company_name} to {new_status}")
        return True
    
    def update_engagement_response(self, contact_name, company, response_text, response_time=None):
        """Update an engagement with response information.
        
        Args:
            contact_name (str): Name of the contact
            company (str): Company name
            response_text (str): The response received
            response_time (float, optional): Response time in hours
        """
        engagements = []
        try:
            with open(self.engagement_file, 'r', newline='') as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                engagements = list(reader)
        except Exception as e:
            self.console.print(f"[bold red]Error:[/bold red] {str(e)}")
            return False
        
        # Find the most recent engagement with this contact/company
        target_engagement = None
        for engagement in reversed(engagements):
            if engagement["Contact Name"] == contact_name and engagement["Company"] == company:
                target_engagement = engagement
                break
        
        if not target_engagement:
            self.console.print(f"[bold yellow]Warning:[/bold yellow] No engagement found for {contact_name} at {company}")
            return False
        
        # Update the engagement
        target_engagement["Response Received"] = response_text
        if response_time:
            target_engagement["Response Time (hours)"] = str(response_time)
        target_engagement["Status"] = "Response received"
        
        # Write updated data back to file
        with open(self.engagement_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(engagements)
        
        self.console.print(f"[bold green]Success:[/bold green] Updated engagement with {contact_name} to include response")
        return True
    
    def generate_analytics(self):
        """Generate analytics from the tracking data and display visualizations."""
        try:
            # Load data into pandas for analysis
            companies_df = pd.read_csv(self.company_file)
            engagements_df = pd.read_csv(self.engagement_file)
            queries_df = pd.read_csv(self.query_file)
            
            # Create analytics console output
            self.console.print("\n[bold blue]===== INTERNSHIP SEARCH ANALYTICS =====[/bold blue]\n")
            
            # Company statistics
            self.console.print("[bold]Company Statistics:[/bold]")
            company_count = len(companies_df)
            industry_counts = companies_df['Industry'].value_counts()
            tech_counts = companies_df['Technologies'].str.split(',').explode().str.strip().value_counts()
            
            table = Table(title="Company Breakdown by Industry")
            table.add_column("Industry", style="cyan")
            table.add_column("Count", style="magenta")
            table.add_column("Percentage", style="green")
            
            for industry, count in industry_counts.items():
                percentage = f"{count/company_count*100:.1f}%"
                table.add_row(industry, str(count), percentage)
            
            self.console.print(table)
            
            # Engagement statistics
            self.console.print("\n[bold]Engagement Statistics:[/bold]")
            platform_counts = engagements_df['Platform'].value_counts()
            type_counts = engagements_df['Engagement Type'].value_counts()
            response_rate = len(engagements_df[engagements_df['Response Received'].notna()]) / len(engagements_df) * 100
            
            table = Table(title="Engagement Breakdown by Platform")
            table.add_column("Platform", style="cyan")
            table.add_column("Count", style="magenta")
            table.add_column("Response Rate", style="green")
            
            for platform in platform_counts.index:
                platform_df = engagements_df[engagements_df['Platform'] == platform]
                platform_response_rate = len(platform_df[platform_df['Response Received'].notna()]) / len(platform_df) * 100
                table.add_row(platform, str(platform_counts[platform]), f"{platform_response_rate:.1f}%")
            
            self.console.print(table)
            self.console.print(f"Overall Response Rate: [bold green]{response_rate:.1f}%[/bold green]")
            
            # Status breakdown
            status_counts = engagements_df['Status'].value_counts()
            self.console.print("\n[bold]Status Breakdown:[/bold]")
            for status, count in status_counts.items():
                self.console.print(f"  {status}: [bold]{count}[/bold] ({count/len(engagements_df)*100:.1f}%)")
            
            # Generate visualizations
            self._generate_visualizations(companies_df, engagements_df, queries_df)
            
            return True
            
        except Exception as e:
            self.console.print(f"[bold red]Error generating analytics:[/bold red] {str(e)}")
            return False
    
    def _generate_visualizations(self, companies_df, engagements_df, queries_df):
        """Generate visualization charts from the tracking data.
        
        Args:
            companies_df (DataFrame): Companies data
            engagements_df (DataFrame): Engagements data
            queries_df (DataFrame): Search queries data
        """
        # Create figures directory if it doesn't exist
        figures_dir = os.path.join(self.data_dir, "figures")
        if not os.path.exists(figures_dir):
            os.makedirs(figures_dir)
        
        # Figure 1: Response rates by platform
        plt.figure(figsize=(10, 6))
        platforms = engagements_df['Platform'].unique()
        response_rates = []
        
        for platform in platforms:
            platform_df = engagements_df[engagements_df['Platform'] == platform]
            response_rate = len(platform_df[platform_df['Response Received'].notna()]) / len(platform_df) * 100
            response_rates.append(response_rate)
        
        plt.bar(platforms, response_rates, color='skyblue')
        plt.xlabel('Platform')
        plt.ylabel('Response Rate (%)')
        plt.title('Response Rates by Platform')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.savefig(os.path.join(figures_dir, 'response_rates_by_platform.png'))
        
        # Figure 2: Engagement status funnel
        plt.figure(figsize=(12, 6))
        status_order = ['Initial Contact', 'Response Received', 'In Conversation', 'Meeting Scheduled', 'Interview Opportunity']
        status_counts = []
        
        for status in status_order:
            count = len(engagements_df[engagements_df['Status'] == status])
            status_counts.append(count)
        
        plt.bar(status_order, status_counts, color='lightgreen')
        plt.xlabel('Status')
        plt.ylabel('Count')
        plt.title('Engagement Funnel')
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(figures_dir, 'engagement_funnel.png'))
        
        # Figure 3: Technologies word cloud (if wordcloud package is available)
        try:
            from wordcloud import WordCloud
            
            # Combine all technologies
            all_techs = ' '.join(companies_df['Technologies'].dropna())
            
            # Generate word cloud
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_techs)
            
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title('Technologies Word Cloud')
            plt.tight_layout()
            plt.savefig(os.path.join(figures_dir, 'technologies_wordcloud.png'))
            
        except ImportError:
            self.console.print("[yellow]Note:[/yellow] WordCloud package not available. Skipping word cloud visualization.")
        
        self.console.print(f"\n[bold green]Success:[/bold green] Generated visualizations in {figures_dir}")
    
    def get_upcoming_actions(self, days=7):
        """Get a list of upcoming actions for the next specified days.
        
        Args:
            days (int): Number of days to look ahead
        """
        try:
            # Load engagement data
            engagements_df = pd.read_csv(self.engagement_file)
            
            # Filter for rows with next action date
            actions_df = engagements_df[engagements_df['Next Action Date'].notna()]
            
            # Convert dates to datetime
            actions_df['Next Action Date'] = pd.to_datetime(actions_df['Next Action Date'])
            
            # Get current date and future cutoff
            today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            cutoff = today + datetime.timedelta(days=days)
            
            # Filter for upcoming actions
            upcoming_df = actions_df[(actions_df['Next Action Date'] >= today) & 
                                    (actions_df['Next Action Date'] <= cutoff)]
            
            # Sort by date
            upcoming_df = upcoming_df.sort_values('Next Action Date')
            
            # Display upcoming actions
            self.console.print(f"\n[bold blue]===== UPCOMING ACTIONS (Next {days} Days) =====[/bold blue]\n")
            
            if len(upcoming_df) == 0:
                self.console.print("[yellow]No upcoming actions scheduled[/yellow]")
                return True
            
            table = Table()
            table.add_column("Date", style="cyan")
            table.add_column("Contact", style="green")
            table.add_column("Company", style="magenta")
            table.add_column("Action", style="yellow")
            
            for _, row in upcoming_df.iterrows():
                date_str = row['Next Action Date'].strftime("%Y-%m-%d")
                table.add_row(
                    date_str,
                    row['Contact Name'],
                    row['Company'],
                    row['Next Action']
                )
            
            self.console.print(table)
            return True
            
        except Exception as e:
            self.console.print(f"[bold red]Error getting upcoming actions:[/bold red] {str(e)}")
            return False
    
    def suggest_optimizations(self):
        """Analyze tracking data and suggest optimizations for the search strategy."""
        try:
            # Load data
            companies_df = pd.read_csv(self.company_file)
            engagements_df = pd.read_csv(self.engagement_file)
            queries_df = pd.read_csv(self.query_file)
            
            suggestions = []
            
            # 1. Platform effectiveness
            platform_response_rates = {}
            for platform in engagements_df['Platform'].unique():
                platform_df = engagements_df[engagements_df['Platform'] == platform]
                if len(platform_df) >= 5:  # Only consider platforms with enough data
                    response_rate = len(platform_df[platform_df['Response Received'].notna()]) / len(platform_df) * 100
                    platform_response_rates[platform] = response_rate
            
            if platform_response_rates:
                best_platform = max(platform_response_rates.items(), key=lambda x: x[1])
                worst_platform = min(platform_response_rates.items(), key=lambda x: x[1])
                
                if best_platform[1] > 1.5 * worst_platform[1]:  # If best is 50% better than worst
                    suggestions.append(f"Focus more on {best_platform[0]} which has a {best_platform[1]:.1f}% response rate compared to {worst_platform[0]}'s {worst_platform[1]:.1f}%")
            
            # 2. Engagement type effectiveness
            type_response_rates = {}
            for eng_type in engagements_df['Engagement Type'].unique():
                type_df = engagements_df[engagements_df['Engagement Type'] == eng_type]
                if len(type_df) >= 5:  # Only consider types with enough data
                    response_rate = len(type_df[type_df['Response Received'].notna()]) / len(type_df) * 100
                    type_response_rates[eng_type] = response_rate
            
            if type_response_rates:
                best_type = max(type_response_rates.items(), key=lambda x: x[1])
                suggestions.append(f"'{best_type[0]}' engagement type has the highest response rate at {best_type[1]:.1f}%. Consider using this approach more frequently.")
            
            # 3. Industry focus
            if 'Industry' in companies_df.columns and 'Contact Status' in companies_df.columns:
                industry_success = {}
                for industry in companies_df['Industry'].unique():
                    industry_df = companies_df[companies_df['Industry'] == industry]
                    if len(industry_df) >= 3:  # Only consider industries with enough data
                        success_rate = len(industry_df[industry_df['Contact Status'].isin(['In Conversation', 'Meeting Scheduled', 'Interview Opportunity'])]) / len(industry_df) * 100
                        industry_success[industry] = success_rate
                
                if industry_success:
                    best_industry = max(industry_success.items(), key=lambda x: x[1])
                    if best_industry[1] > 0:  # Only suggest if there's some success
                        suggestions.append(f"Companies in the {best_industry[0]} industry show higher engagement rates ({best_industry[1]:.1f}%). Consider focusing more on this sector.")
            
            # 4. Technology focus
            if 'Technologies' in companies_df.columns:
                # Extract all technologies
                all_techs = companies_df['Technologies'].str.split(',').explode().str.strip()
                tech_counts = all_techs.value_counts()
                
                if not tech_counts.empty:
                    top_tech = tech_counts.index[0]
                    suggestions.append(f"{top_tech} appears most frequently in job requirements. Ensure your portfolio highlights projects using this technology.")
            
            # 5. Response time analysis
            if 'Response Time (hours)' in engagements_df.columns:
                response_times = pd.to_numeric(engagements_df['Response Time (hours)'], errors='coerce')
                if not response_times.empty and not response_times.isna().all():
                    avg_response_time = response_times.mean()
                    suggestions.append(f"Average response time is {avg_response_time:.1f} hours. Plan to follow up if no response within {max(48, 2*avg_response_time):.0f} hours.")
            
            # Display suggestions
            self.console.print("\n[bold blue]===== STRATEGY OPTIMIZATION SUGGESTIONS =====[/bold blue]\n")
            
            if not suggestions:
                self.console.print("[yellow]Not enough data yet to make optimization suggestions. Continue collecting more engagement data.[/yellow]")
                return True
            
            for i, suggestion in enumerate(suggestions, 1):
                self.console.print(f"[bold]{i}.[/bold] {suggestion}")
            
            return True
            
        except Exception as e:
            self.console.print(f"[bold red]Error generating optimization suggestions:[/bold red] {str(e)}")
            return False

# Example usage
if __name__ == "__main__":
    tracker = InternshipSearchTracker()
    
    # Add example data for demonstration
    tracker.add_company({
        "Company Name": "Example Tech",
        "Industry": "Software",
        "Company Size": "201-1000",
        "Technologies": "Python, Java, AWS",
        "Engineering Manager Name": "Jane Smith",
        "Engineering Manager LinkedIn": "linkedin.com/in/janesmith",
        "Contact Status": "Initial Research"
    })
    
    tracker.add_engagement({
        "Contact Name": "Jane Smith",
        "Company": "Example Tech",
        "Position": "Engineering Manager",
        "Platform": "LinkedIn",
        "Engagement Type": "Comment",
        "Content Sent": "Great insights on API design! I recently built a similar system using Python.",
        "Next Action": "Follow up with portfolio",
        "Next Action Date": (datetime.datetime.now() + datetime.timedelta(days=2)).strftime("%Y-%m-%d"),
        "Status": "Initial Contact"
    })
    
    # Generate reports
    tracker.get_upcoming_actions()
    tracker.generate_analytics()
    tracker.suggest_optimizations()
