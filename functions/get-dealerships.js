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
async function main(params) {
    const cloudant = getCloudantAccount(params);
    const cloudantDb = cloudant.db.use('dealerships');
    const list = await cloudantDb.list({ include_docs: true })
    return {
        entries: list.rows.map((row) => {
            return {
                id: row.doc.id,
                city: row.doc.city,
                state: row.doc.state,
                st: row.doc.st,
                address: row.doc.address,
                zip: row.doc.zip,
                lat: row.doc.lat,
                long: row.doc.long
            }
        })
    };
}

function getCloudantAccount(params) {
    if (!params.host) return Promise.reject('host parameter is required.');
    if (!params.iamApiKey) return Promise.reject('iamApiKey parameter is required.');
    if (!params.iamUrl) return Promise.reject('iamUrl parameter is required.');
    const Cloudant = require('@cloudant/cloudant');
    return new Cloudant({
        url: `https://${params.host}`,
        plugins: { iamauth: { iamApiKey: params.iamApiKey, iamTokenUrl: params.iamUrl }}
    });
}
