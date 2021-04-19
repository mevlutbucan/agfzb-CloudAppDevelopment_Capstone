/**
 * ### Description
 * Get all documents in Cloudant database:
 * https://docs.couchdb.org/en/stable/api/database/bulk-api.html#db-all-docs
 * 
 * ### Parameters
 * - **_dbName_** (string): `Required`
 * - **_params_** (json): `Optional`
 *  - **_include_docs_** (boolean): Include the full content of the design documents in the return. Default is `false`.
 *  - **_limit_** (number): Limit the number of the returned design documents to the specified number. `Optional`
 **/
function main(message) {
    if (!message.host) return Promise.reject('host parameter is required.');
    if (!message.iamApiKey) return Promise.reject('iamApiKey parameter is required.');
    if (!message.iamUrl) return Promise.reject('iamUrl parameter is required.');
    const cloudant = getCloudantAccount(message);
    if (!message.dbName) return Promise.reject('dbName parameter is required.');
    const cloudantDb = cloudant.db.use(message.dbName);
    return listAllDocuments(cloudantDb, message.params);
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
