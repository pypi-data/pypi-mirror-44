# 调用solidity智能协约的SDK

需要python3.6的环境

## 安装virtualenv
```bash
$ pip install virtualenv
$ virtualenv --no-site-packages venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
```

## 便于开发SDK的使用方式
```bash
$ cd $youProjPath
$ . ./venv/bin/activiate
$ cd $pyconstractsdk_path
$ python setup.py develop

```

## 使用的第三方的加密解密模块
```bash
$ npm i -g crypto-tx
```