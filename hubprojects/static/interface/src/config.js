let baseUrl = ''
if (process.env.NODE_ENV === 'production') {
   baseUrl = 'http://localhost:5000';
} else {
   baseUrl = 'http://localhost:5000';
}

export const apiPath = baseUrl;
