xpath2err = "http://www.w3.org/2005/xqt-errors"
xdtSchemaErrorNS = "http://www.xbrl.org/2005/genericXmlSchemaError"
errMsgPrefixNS: dict[str | None, str] = {  # err prefixes which are not declared, such as XPath's "err" prefix
    "err": xpath2err,
    "xmlSchema": xdtSchemaErrorNS,
    "utre": "http://www.xbrl.org/2009/utr/errors",
}
errMsgNamespaceLocalNameMap: dict[str | None, dict[str, str]] = {
    xdtSchemaErrorNS: {
        "valueError": "XmlSchemaError",
    },
}
