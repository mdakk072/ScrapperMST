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
        this.connectSocket();
    },
    methods: {
        connectSocket() {
            const socket = io('http://localhost:7705');
            
            socket.on('scraper_status', (data) => {
                this.scrapers = data;
                this.loading = false;
            });

            socket.on('profiles_status', (data) => {
                this.profiles = data;
            });

            socket.on('disconnect', () => {
                console.log('WebSocket disconnected.');
            });
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
