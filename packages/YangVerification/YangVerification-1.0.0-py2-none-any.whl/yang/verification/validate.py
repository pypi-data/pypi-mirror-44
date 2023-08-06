# coding=utf-8
import vlan_schema
import vlan_ip_schema
import pyangbind.lib.pybindJSON as pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
import json
import traceback
from pyangbind.lib.xpathhelper import YANGPathHelper


def start_check(type, action, target,hostname, options=None):
    msg = "ok"
    module = type + "_check"
    msg = globals().get(module)(action, target, hostname)
    return msg


def vlan_check(action, target, hostname):
    ph = YANGPathHelper()
    try:
        ## 返回的是一个Json对象
        current_vlan = get_current_vlan(ph, hostname)
    except Exception, e:
        print traceback.format_exc(e)
        return "设备上配置未通过yang model检测"

    if action == "add":
        ## 如果是增则对 先检查整体添加完后是否符合yang model 然后对所有相关的key进行逐一增加检查
        try:

            additional =  pybindJSON.loads(target, vlan_ip_schema, "vlan_ip_schema",  path_helper=ph)
            # additional1 = pybindJSONDecoder.load_json(target, vlan_ip_schema, "vlan_ip_schema", path_helper=ph)
            # mergeConfig = dict(json.loads(current_vlan))
            # mergeConfig.update(dict(json.loads(pybindJSON.dumps(additional))))
            # print json.dumps(mergeConfig)
            # afterConfig = pybindJSON.loads(mergeConfig,  vlan_schema, "vlan_schema", path_helper=ph)
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测"

        return check_add(target, json.loads(pybindJSON.dumps(current_vlan)))



def get_current_vlan(ph,hostname):
    ### 这里预留获取逻辑 直接在task上实现或者如果校验是个模板的话则调用get模板来实现
    ### 暂时只能用北向api来实现
    result = get_vlan_config(hostname)
    current_vlan = pybindJSON.loads(result, vlan_schema, "vlan_schema",  path_helper=ph)
    return current_vlan

def get_vlan_config(hostname):
    import requests
    url = "http://100.67.166.36:19999/apidoc/get_vlan?hostname=" + hostname
    res = requests.get(url)
    print res.content
    response = json.loads(res.content)

    if response.get("code", -1) != 0:
        raise ValueError("获取实时配置失败")
    conifg = {
        "VLAN":response.get("data")
    }
    return conifg

def check_add(target, current):
    ## 新增只允许新增ipAddress
    ip_types = ["ipv4Address", "ipv6Address"]
    try:
        addtional = target["VLAN_IP"]
        base = current["VLAN"]
        for k in addtional.keys():
            vlan_base_ipAddress = base[k]["ipAddress"]
            addtional_ipAddress = addtional[k]["ipAddress"]
            for ip_type in ip_types:
                if addtional_ipAddress.get(ip_type, []) and vlan_base_ipAddress.get(ip_type,[]):
                    for ip in addtional_ipAddress[ip_type]:
                        if ip in vlan_base_ipAddress[ip_type]:
                            return "存在重复ip" + ip
                    vlan_base_ipAddress[ip_type].extend(addtional_ipAddress[ip_type])
                elif not addtional_ipAddress.get(ip_type, []):
                    continue
                else:
                    vlan_base_ipAddress[ip_type] = addtional_ipAddress[ip_type]

        print current
        pybindJSON.loads(current, vlan_schema, "vlan_schema", path_helper=YANGPathHelper())
        return "ok"
    except Exception,e:
        print traceback.format_exc(e)
        return "yang model转换失败,请检查配置"






if __name__ == "__main__":
    config = get_vlan_config("11.161.62.23")
    print config
    # target = {"VLAN_IP": {
    #     "VLAN10": {
    #         "ipAddress": {
    #             # "ipv4Address": ["11.210.88.1/30", "192.168.0.1/30"],
    #             "ipv6Address": ["fe00::4/64", "fe00::3/64"]
    #         }
    #     }
    # }
    # }
    # options = []
    # msg = start("vlan", "add", target, options)
    # print msg