## spark-operator-image-tool
[![Build status](https://travis-ci.org/Jiri-Kremser/spark-operator-image-tool.svg?branch=master)](https://travis-ci.org/Jiri-Kremser/spark-operator-image-tool)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](http://www.apache.org/licenses/LICENSE-2.0)

Purpose of this tool is to verify if given container image is compatible with [spark-operator](https://github.com/radanalyticsio/spark-operator).

### Installation

```
pip3 install soit --user
```

### Quick Start

```
soit --image quay.io/jkremser/openshift-spark --tag 2.4.0
```
