var baseURL = 'http://localhost';
if (process.env.NODE_ENV == 'development') {
    baseURL = 'http://localhost';
}

const config = {
    loginFieldName: "phone",
    backendBaseURL: baseURL,
    requestTimeout: 10000,
//    defaultLangCode: "zh-hans",
    defaultLangCode: "en",
}


export default config
