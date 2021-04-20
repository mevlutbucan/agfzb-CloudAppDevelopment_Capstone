/**
 * Get sentiment result of review from Watson NLU service:
 * https://cloud.ibm.com/apidocs/natural-language-understanding
 */
function main(params) {
    const nluOrError = getNLUInstance(params);
    if (typeof nluOrError === 'string') return Promise.reject({ error: nluOrError });
    const analyzeParams = getAnalyzeParameters(params);
    return nluOrError.analyze(analyzeParams)
        .then(({ result }) => Promise.resolve(result.sentiment.document))
        .catch(err => Promise.reject({ error: err.message }));
}

function getNLUInstance(params) {
    if (!params.apiKey) return 'apiKey parameter is required.';
    if (!params.serviceUrl) return 'serviceUrl parameter is required.';
    const NaturalLanguageUnderstanding = require("ibm-watson/natural-language-understanding/v1");
    const { IamAuthenticator } = require("ibm-watson/auth");
    return new NaturalLanguageUnderstanding({
        version: "2021-04-20",
        authenticator: new IamAuthenticator({ apikey: params.apiKey }),
        serviceUrl: params.serviceUrl
    });
}

function getAnalyzeParameters(params) {
    return {
        'text': params.text,
        'features': {
            'sentiment': {}
        }
    };
}
