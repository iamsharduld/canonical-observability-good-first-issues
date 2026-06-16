#!/bin/bash
# loki-operators #80 repro — run lokitool inside the coordinator charm container (where the charm runs it).
M="gfi-k8s:testing"; U="loki-coordinator-k8s/0"
CD="/var/lib/juju/agents/unit-loki-coordinator-k8s-0/charm"
LOG=/tmp/repro80.log; : > "$LOG"; exec > >(tee -a "$LOG") 2>&1
echo "### start $(date +%T)"

echo "== worker pod IP (loki API :3100) =="
WIP=$(microk8s kubectl get pods -n testing -o wide --no-headers 2>/dev/null | awk '/loki-worker/{print $6; exit}')
echo "WIP=$WIP"
ADDR="http://$WIP:3100"

echo "== lokitool present in charm container =="
timeout 40 juju exec -m "$M" --unit "$U" -- sh -c "cd $CD && pwd && ls -la lokitool && ./lokitool --version 2>&1 | head -1"

echo "== write rule files into container =="
mkdir -p /tmp/r
cat > /tmp/r/valid.yaml <<'EOF'
groups:
- name: valid_group
  rules:
  - alert: ValidAlert
    expr: 'sum(count_over_time({job="test"} |= "error" [5m])) > 0'
    for: 5m
    labels: {severity: warning}
    annotations: {summary: "valid rule"}
EOF
cat > /tmp/r/invalid.yaml <<'EOF'
groups:
- name: invalid_group
  rules:
  - alert: BadAlert
    expr: 'this is (((not valid logql'
    labels: {severity: warning}
EOF
V=$(base64 -w0 /tmp/r/valid.yaml); I=$(base64 -w0 /tmp/r/invalid.yaml)
timeout 40 juju exec -m "$M" --unit "$U" -- sh -c "echo $V | base64 -d > /tmp/valid.yaml; echo $I | base64 -d > /tmp/invalid.yaml; ls -l /tmp/valid.yaml /tmp/invalid.yaml"

echo
echo "############ TEST A: lokitool rules sync valid+invalid (coordinator's exact call) ############"
timeout 40 juju exec -m "$M" --unit "$U" -- sh -c "cd $CD && ./lokitool rules sync /tmp/valid.yaml /tmp/invalid.yaml --address=$ADDR --id=fake; echo exitA=\$?"
echo "---- rules in loki after the combined sync ----"
timeout 30 juju exec -m "$M" --unit "$U" -- sh -c "cd $CD && ./lokitool rules list --address=$ADDR --id=fake 2>&1 | head -15"

echo
echo "############ TEST B: lokitool rules sync valid ONLY ############"
timeout 40 juju exec -m "$M" --unit "$U" -- sh -c "cd $CD && ./lokitool rules sync /tmp/valid.yaml --address=$ADDR --id=fake; echo exitB=\$?"
echo "---- rules in loki after valid-only sync ----"
timeout 30 juju exec -m "$M" --unit "$U" -- sh -c "cd $CD && ./lokitool rules list --address=$ADDR --id=fake 2>&1 | head -15"
echo "### done $(date +%T)"
