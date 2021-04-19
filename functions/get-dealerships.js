/**
 * Get all documents in Cloudant database:
 * https://docs.cloudant.com/database.html#get-documents
 **/

function main(message) {
    const cloudant = getCloudantAccount(message);
    if (!message.dbName) {
        return Promise.reject('dbname is required.');
    }
    const cloudantDb = cloudant.db.use(message.dbName);
    let params = {};
    if (typeof message.params === 'object') {
        params = message.params;
    } else if (typeof message.params === 'string') {
        try {
            params = JSON.parse(message.params);
        } catch (e) {
            return Promise.reject('params field cannot be parsed. Ensure it is valid JSON.');
        }
    }
    return listAllDocuments(cloudantDb, params);
}

/**
 * List all documents.
 */
function listAllDocuments(cloudantDb, params) {
    return new Promise(function (resolve, reject) {
        cloudantDb.list(params, function (error, response) {
            if (!error) {
                resolve(response);
            } else {
                console.error("error", error);
                reject(error);
            }
        });
    });
}

function getCloudantAccount(params) {
    const Cloudant = require('@cloudant/cloudant');
    return new Cloudant({
        url: `https://${params.host}`,
        plugins: { iamauth: { iamApiKey: params.iamApiKey, iamTokenUrl: params.iamUrl }}
    });
}
