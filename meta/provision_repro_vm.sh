#!/bin/bash
# Provision a dedicated VM for reproducing loki-operators #80 and istio-beacon #42
# (kept isolated from the live `cos` VM).
set -x
multipass launch 24.04 --name gfi-repro --cpus 8 --memory 16G --disk 80G || exit 1
run() { multipass exec gfi-repro -- bash -c "$1"; }
run 'sudo snap install microk8s --classic --channel=1.30-strict/stable'
run 'sudo usermod -a -G snap_microk8s ubuntu'
run 'sudo microk8s status --wait-ready'
run 'sudo microk8s enable hostpath-storage dns'
run 'sudo microk8s enable metallb:10.64.140.43-10.64.140.49'
run 'sudo snap install juju --channel=3/stable'
run 'sg snap_microk8s -c "juju bootstrap microk8s gfi-k8s --model-default automatically-retry-hooks=false"'
run 'sg snap_microk8s -c "juju add-model testing"'
run 'sg snap_microk8s -c "juju status"'
echo "PROVISION_DONE"
