const app = Vue.createApp({
    data() {
        return {
            scrapers: {}, // Scraper data
            profiles: {}, // Profile data
            loading: true, // Loading state
        };
    },
    delimiters: ['[[', ']]'], // To avoid conflict with Jinja2 templates
    mounted() {
        this.fetchStatusData();
        setInterval(this.fetchStatusData, 1000);  // Fetch data every 5 seconds
    },
    methods: {
        fetchStatusData() {
            console.log('Fetching status data...');
            
            // Fetch both scraper and profile status from the /api/status endpoint
            fetch('http://10.0.0.110:7777/api/status')
                .then(response => response.json())
                .then(data => {
                    console.log('Received status data:', data);
                    this.scrapers = data.scraper_status;  // Set scrapers data
                    this.profiles = data.profiles_status;  // Set profiles data
                    this.loading = false;
                })
                .catch(error => console.error('Error fetching status data:', error));
        },
        formatDate(dateString) {
            return new Date(dateString).toLocaleString();
        },
        formatDuration(durationString) {
            return durationString ? durationString.split('.')[0] : 'N/A';
        },
        profile_name(profile) {
            return profile.config_file.split('/').slice(-1)[0].split('.')[0]; // Extract profile name from config file
        }
    }
});

app.mount('#homeapp');
