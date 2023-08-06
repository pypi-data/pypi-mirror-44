function generate_production_request_guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }

    return s4() + s4() + s4();
}

function formatDate(d) {
    return (
        d.getFullYear() + '-' + d.getMonth() + '-' + d.getDate() + ' ' +
        d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds() + '.' +
        d.getMilliseconds())
}

// Общий UUID клиента для всех запросов
var clientUUID = generate_production_request_guid();
var productionRequestLogStore = [];
var productionRequestExcludeUrls = [];

XhrInterceptor.addRequestCallback(function(xhr) {
    try {
        xhr.setRequestHeader('PR-UUID', clientUUID + '#' + generate_production_request_guid());
        xhr.setRequestHeader('PR-STARTED', Date.now());
    } catch (e) {
        console.log("Can't set production request headers. Details:", e.error.toString());
    }
});

XhrInterceptor.addResponseCallback(function(xhr) {
    try {
        var req_uuid = xhr.getResponseHeader('PR-UUID');
        var req_started = xhr.getResponseHeader('PR-STARTED');
        if (req_uuid && req_started) {
            req_started = parseInt(req_started, 10);
            var addToLog = true;

            if (productionRequestExcludeUrls.length) {
                for (var i = 0; i < productionRequestExcludeUrls.length; i++) {
                    if (xhr.responseURL.indexOf(productionRequestExcludeUrls[i]) !== -1) {
                        addToLog = false;
                        break;
                    }
                }
            }

            var s_total = parseFloat(xhr.getResponseHeader('PR-S-TOTAL') || 0);
            var s_sql_total = parseFloat(xhr.getResponseHeader('PR-S-SQL-TOTAL') || 0);

            if (addToLog) {
                var record = {
                    'uuid': req_uuid,
                    'c_started': formatDate(new Date(req_started)),
                    'c_path': xhr.responseURL,
                    'c_total': Math.max(Date.now() - req_started, s_total, 0),
                    's_started': xhr.getResponseHeader('PR-S-STARTED') || '',
                    's_path': xhr.getResponseHeader('PR-S-PATH') || '',
                    's_user': xhr.getResponseHeader('PR-S-USER') || '',
                    's_hostname': xhr.getResponseHeader('PR-S-HOSTNAME') || '',
                    's_total': s_total,
                    's_sql_total': s_sql_total,
                    's_sql_s_total': parseFloat(xhr.getResponseHeader('PR-S-SQL-S-TOTAL') || 0),
                    's_sql_i_total': parseFloat(xhr.getResponseHeader('PR-S-SQL-I-TOTAL') || 0),
                    's_sql_u_total': parseFloat(xhr.getResponseHeader('PR-S-SQL-U-TOTAL') || 0),
                    's_sql_d_total': parseFloat(xhr.getResponseHeader('PR-S-SQL-D-TOTAL') || 0),
                    's_sql_c_total': parseFloat(xhr.getResponseHeader('PR-S-SQL-C-TOTAL') || 0),
                    's_sql_count': parseInt(xhr.getResponseHeader('PR-S-SQL-COUNT') || 0),
                    's_sql_s_count': parseInt(xhr.getResponseHeader('PR-S-SQL-S-COUNT') || 0),
                    's_sql_i_count': parseInt(xhr.getResponseHeader('PR-S-SQL-I-COUNT') || 0),
                    's_sql_u_count': parseInt(xhr.getResponseHeader('PR-S-SQL-U-COUNT') || 0),
                    's_sql_d_count': parseInt(xhr.getResponseHeader('PR-S-SQL-D-COUNT') || 0),
                    's_sql_c_count': parseInt(xhr.getResponseHeader('PR-S-SQL-C-COUNT') || 0),
                    's_sql_sp_count': parseInt(xhr.getResponseHeader('PR-S-SQL-SP-COUNT') || 0),
                    's_sql_j_count': parseInt(xhr.getResponseHeader('PR-S-SQL-J-COUNT') || 0),
                    's_sql_di_count': parseInt(xhr.getResponseHeader('PR-S-SQL-DI-COUNT') || 0),
                    's_sql_gb_count': parseInt(xhr.getResponseHeader('PR-S-SQL-GB-COUNT') || 0),
                    's_sql_transaction_count': parseInt(xhr.getResponseHeader('PR-S-SQL-TRANSACTION-COUNT') || 0),
                    's_sql_transaction_total': parseFloat(xhr.getResponseHeader('PR-S-SQL-TRANSACTION-TOTAL') || 0),
                    's_app_total': s_total - s_sql_total,
                    's_client_ip': xhr.getResponseHeader('PR-S-CLIENT-IP') || '',
                    's_pid': xhr.getResponseHeader('PR-S-PID') || '',
                    's_uss': parseFloat(xhr.getResponseHeader('PR-S-USS') || 0),
                    's_pss': parseFloat(xhr.getResponseHeader('PR-S-PSS') || 0),
                    's_swap': parseFloat(xhr.getResponseHeader('PR-S-SWAP') || 0),
                    's_rss': parseFloat(xhr.getResponseHeader('PR-S-RSS') || 0),
                };
                record['tr_total'] = (record['c_total'] - record['s_total']).toFixed(3);
                productionRequestLogStore.push(record);
            }
        }
    } catch (e) {
        console.log("Can't process production response. Details:", e.error.toString());
    }
});
// Подключаемся к запросам
XhrInterceptor.wire();

function startLogging(clientLogUrl, timeout = 10000) {
    function sendProductionRequestStats() {
        if (productionRequestLogStore.length) {
            var log_part = productionRequestLogStore.slice();
            productionRequestLogStore = [];
            Ext.Ajax.request({
                url: clientLogUrl,
                method: 'POST',
                params: {
                    logs: Ext.util.JSON.encode(log_part)
                },
                success: function (response) {
                },
                failure: function () {
                    productionRequestLogStore.concat(log_part)
                }
            });
        }
    }

    productionRequestExcludeUrls.push(clientLogUrl);
    setInterval(sendProductionRequestStats, timeout);
}