const url = {
    getUrlWithOutParams: function (url) {
        return url.split("?")[0];
    },
    getUrlWithoutParamsAndHash: function (url) {
        return this.getUrlWithOutParams(url).split("#")[0];
    },
    getServerAddress: function (url) {
        var rUrl = this.getUrlWithOutParams(url);
        var checkArr = rUrl.split("://");
        if (checkArr.length == 2) {
            var i = checkArr[1].indexOf("/");
            if (i == -1) {
                return rUrl;
            } else {
                return checkArr[0] + "://" + checkArr[1].substring(0, i);
            }
        }
        return "";
    },
    getQueryStr: function (url) {
        var i = url.indexOf("?");
        if (i != -1) {
            return url.substring(i + 1, url.length);
        }
        return null;
    },
    getParameterInUrl: function (url, paraName) {
        return this.getParameterInQueryStr(this.getQueryStr(url), paraName);
    },
    getParameterInQueryStr: function (queryStr, paraName) {
        if (queryStr) {
            var a = /\+/g;
            var reg = new RegExp("(^|&)" + paraName + "=([^&]*)(&|$)");
            var r = queryStr.match(reg);
            if (r != null) {
                return decodeURIComponent(r[2].replace(a, " "));
            }
        }

        return null;
    },
    getAllParametersFromUrl: function (url) {
        return this.getAllParametersFromQueryStr(this.getQueryStr(url));
    },
    getAllParametersFromQueryStr: function (queryStr) {
        var params = {};
        if (queryStr) {
            var e,
            a = /\+/g,  // Regex for replacing addition symbol with a space
            r = /(^|&)(.+?)=([^&]*)(&|$)/g,
            d = function (s) { return decodeURIComponent(s.replace(a, " ")); },
            q = queryStr;

            while (e = r.exec(q)) {
                params[d(e[2])] = d(e[3]);
            }
        }
        return params;
    },
    appendParameterInUrl: function (url, paraName, paramValue) {
        var queryStr = this.getQueryStr(url)
        if (!queryStr) {
            queryStr = ""
        }
        queryStr = this.appendParameterInQueryStr(queryStr, paraName, paramValue);
        return this.getUrlWithOutParams(url) + "?" + queryStr;
    },
    appendParameterInQueryStr: function (queryStr, paraName, paramValue) {
        var ret = queryStr;
        if (ret) {
            ret += "&";
        }
        ret += paraName + "=" + paramValue;
        return ret;
    },
    changeParamValueInUrl: function (url, paramName, replaceWith) {
        var ret = this.getUrlWithOutParams(url);
        var queryStr = this.getQueryStr(url);
        if (queryStr) {
            ret += "?" + this.changeParamValueInQueryStr(queryStr, paramName, replaceWith);
        }
        return ret;
    },
    changeParamValueInQueryStr: function (queryStr, paramName, replaceWith) {
        var ret = "";
        if (queryStr) {
            var re = eval('/(' + paramName + '=)([^&]*)/gi');
            ret += queryStr.replace(re, paramName + '=' + replaceWith);
        }
        return ret;
    },
    changeParamNameAndItsValueInUrl: function (url, paramName, paramValue, newParamName, newParamValue) {
        var ret = this.getUrlWithOutParams(url);
        var queryStr = this.getQueryStr(url);
        if (queryStr) {
            ret += "?" + this.changeParamNameAndItsValueInQueryStr(queryStr, paramName, newParamName, newParamValue);
        }
        return ret;
    },
    changeParamNameAndItsValueInQueryStr: function (queryStr, paramName, paramValue, newParamName, newParamValue) {
        var ret = "";
        if (queryStr) {
            var re = eval('/(' + paramName + '=)('+ paramValue + ')/gi');
            ret += queryStr.replace(re, newParamName + '=' + newParamValue);
        }
        return ret;
    },
    base64EncodeParamsInUrl: function(url) {
        if (url) {
            var ret = this.getUrlWithOutParams(url);
            var queryStr = this.getQueryStr(url);
            if (queryStr) {
                ret += "?" + this.base64EncodeParamsInQueryStr(queryStr);
            }
            return ret;
        }
        return url;
    },
    base64EncodeParamsInQueryStr: function(queryStr) {
        if (queryStr) {
            var ret = queryStr;
            var allParams = this.getAllParameters(queryStr);
            var hasParams = false;
            if (allParams) {
                for (var i in allParams) {
                    ret = this.replaceParam(ret, i, allParams[i], $.base64.encode(i), $.base64.encode(allParams[i]));
                }
                hasParams = true;
            }
            if (hasParams) {
                ret = ret + "&bpvs=true";
            } else {
                ret = ret + "bpvs=true";
            }
            return ret;
        }
        return queryStr;
    },
}
const cookie = {
    /**
     * @param: _key，键名；
     * @param: _val，键值；
     * @param: _day，有效天数；
     * @param: _path，作用路径；
     */
    //cookie赋值
set: function (_key, _val, _day, _path) {
        var str, obj;

        if (!_key) {
            return;
        }

        str = _key +'='+ escape(_val);

        if (_day && !isNaN(_day)) {
            obj = new Date();
            obj.setTime(obj.getTime() + _day*24*60*60*1000);
            str += ';expires='+ obj.toGMTString();
        }

        if (_path) {
            str += ';path='+ _path;
        }

        document.cookie = str;
    },
    /**
     * @param: _key，键名；
     */
    //cookie取值
    get: function (_key) {
        var str;

        if (!_key) {
            return '';
        }

        str = document.cookie.match(new RegExp("(^| )" + _key + "=([^;]*)(;|$)"));

        if(str) {
            str = unescape(str[2]);
            if (str == 'undefined') {
                str = ''
            }
            return str;
        } else {
            return '';
        }
    },
    /**
     * @param: _key，键名；
     * @param: _path，作用路径；
     */
    //cookie删除
    del: function (_key, _path) {
        this.set(_key, '', '-1', _path);
    }
}

const loader = {
    loadjs: function(filename, callback){
        var fileref=document.createElement('script')
        fileref.setAttribute("type","text/javascript")
        fileref.setAttribute("src", filename)
  
        if (typeof fileref!="undefined") {
            document.getElementsByTagName("head")[0].appendChild(fileref)
            if(typeof callback == 'function') {
                fileref.onload = function(){
                    callback();
                }
            }
        }
    },
    loadcss: function(filename, callback) {
        var fileref=document.createElement("link")
        fileref.setAttribute("rel", "stylesheet")
        fileref.setAttribute("type", "text/css")
        fileref.setAttribute("href", filename)
        if (typeof fileref!="undefined") {
            document.getElementsByTagName("head")[0].appendChild(fileref)
            if(typeof callback == 'function') {
                fileref.onload = function(){
                    callback();
                }
            }
        }        
    },
}

const logstr = function (obj) {
    var log = ""
    for (var key in obj) {
        log = "[" + key + "] " + obj[key] + ".\n"
    }
    return log
}


const date = {
    formatLocaleDateTime: function(dateStr) {
        var d = new Date(dateStr)
        return [d.toLocaleDateString(), d.toLocaleTimeString()].join(" ")
    },
    formatLocaleDate: function(dateStr) {
        var d = new Date(dateStr)
        return d.toLocaleDateString()
    },
    formatLocaleTime: function(dateStr) {
        var d = new Date(dateStr)
        return d.toLocaleTimeString()
    },
}

export default {
    url, cookie, loader, logstr, date
}
