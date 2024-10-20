const app = Vue.createApp({
    data() {
        return {
            scrapers: {
                1: { id: 1, name: 'Scraper 1', status: 'Active', duration: '1:30:00', profile_name: 'Profile 1' },
                2: { id: 2, name: 'Scraper 2', status: 'Inactive', duration: '0:45:30', profile_name: 'Profile 1' },
                3: { id: 3, name: 'Scraper 3', status: 'Active', duration: '2:15:45', profile_name: 'Profile 2' }
            },
            profiles: {
                1: { id: 1, name: 'Profile 21', status: 'Active', last_updated: '2023-09-26T10:30:00Z' },
                2: { id: 2, name: 'Profile 2', status: 'Inactive', last_updated: '2023-09-25T15:45:00Z' }
            },
            loading: false,
        };
    },
    delimiters: ['[[', ']]'],
    methods: {
        getScrapersByProfile(profileName) {
            return Object.values(this.scrapers).filter(scraper => scraper.profile_name === profileName);
        },
        formatDate(dateString) {
            const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
            return new Date(dateString).toLocaleDateString(undefined, options);
        },
        formatDuration(durationString) {
            if (durationString) {
                return durationString.split('.')[0]; // Remove milliseconds from duration
            }
            return ''; // Return an empty string if durationString is undefined
        }
    }
});

app.mount('#home');