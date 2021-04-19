/**
 * Get all documents in Cloudant database:
 * https://docs.couchdb.org/en/stable/api/database/bulk-api.html#db-all-docs
 **/
async function main(params) {
    const cloudantOrError = getCloudantAccount(params);
    if (typeof cloudantOrError === 'string') return Promise.reject(cloudantOrError);
    const cloudantDb = cloudantOrError.db.use('dealerships');
    const list = await cloudantDb.list({ include_docs: true });
    const filteredList = getFilteredList(list, params);
    return getFormattedList(filteredList);
}

function getCloudantAccount(params) {
    if (!params.host) return 'host parameter is required.';
    if (!params.iamApiKey) return 'iamApiKey parameter is required.';
    if (!params.iamUrl) return 'iamUrl parameter is required.';
    const Cloudant = require('@cloudant/cloudant');
    return new Cloudant({
        url: `https://${params.host}`,
        plugins: { iamauth: { iamApiKey: params.iamApiKey, iamTokenUrl: params.iamUrl }}
    });
}

function getFilteredList(list, params) {
    if (params.state === undefined) return list.rows;
    if (typeof params.state === 'string')
        return list.rows.filter(row => row.doc.st === params.state);
}

function getFormattedList(rows) {
    return {
        entries: rows.map((row) => {
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
