#!/usr/bin/env bash
set -u

usage() {
  cat <<'USAGE'
Usage:
  init-ai-project.sh /path/to/project [--link-skill skill-name ...] [--skills-root /path/to/codex-skills]

Creates the AI Project Workflow directories and starter templates in an existing project.
Safe to rerun: existing files are skipped, not overwritten.

Options:
  --link-skill NAME      Link a selected skill into TARGET/.agents/skills/NAME.
  --skills-root PATH     Directory containing skill source folders. Defaults to CODEX_SKILLS_ROOT,
                         then to a sibling codex-skills directory beside this template.
  --help                 Show this help.
USAGE
}

if [ "$#" -eq 0 ]; then
  usage
  exit 2
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TEMPLATE_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TARGET=""
SKILLS_ROOT="${CODEX_SKILLS_ROOT:-}"
LINK_SKILLS=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    --help)
      usage
      exit 0
      ;;
    --link-skill)
      if [ "$#" -lt 2 ]; then
        echo "FAIL missing value for --link-skill"
        exit 2
      fi
      LINK_SKILLS+=("$2")
      shift 2
      ;;
    --skills-root)
      if [ "$#" -lt 2 ]; then
        echo "FAIL missing value for --skills-root"
        exit 2
      fi
      SKILLS_ROOT="$2"
      shift 2
      ;;
    -*)
      echo "FAIL unknown option: $1"
      exit 2
      ;;
    *)
      if [ -n "$TARGET" ]; then
        echo "FAIL multiple target paths supplied"
        exit 2
      fi
      TARGET="$1"
      shift
      ;;
  esac
done

if [ -z "$TARGET" ]; then
  echo "FAIL target project path is required"
  exit 2
fi

if [ ! -d "$TARGET" ]; then
  echo "FAIL target project does not exist: $TARGET"
  exit 1
fi

if [ -z "$SKILLS_ROOT" ] && [ -d "$TEMPLATE_ROOT/../codex-skills" ]; then
  SKILLS_ROOT="$(cd "$TEMPLATE_ROOT/../codex-skills" && pwd)"
fi

if [ -n "$SKILLS_ROOT" ]; then
  if [ -d "$SKILLS_ROOT" ]; then
    SKILLS_ROOT="$(cd "$SKILLS_ROOT" && pwd)"
  else
    echo "WARN skills root does not exist: $SKILLS_ROOT"
  fi
fi

mkdir_report() {
  if [ -d "$1" ]; then
    echo "SKIPPED dir $1"
  else
    mkdir -p "$1"
    echo "CREATED dir $1"
  fi
}

copy_if_missing() {
  src="$1"
  dest="$2"
  if [ -e "$dest" ]; then
    echo "SKIPPED file $dest"
  else
    cp "$src" "$dest"
    echo "CREATED file $dest"
  fi
}

mkdir_report "$TARGET/.ai"
for dir in context requirements plans decisions handoffs verification knowledge templates; do
  mkdir_report "$TARGET/.ai/$dir"
done
mkdir_report "$TARGET/docs"
mkdir_report "$TARGET/.agents"
mkdir_report "$TARGET/.agents/skills"
mkdir_report "$TARGET/.ai/agents"
mkdir_report "$TARGET/.ai/runs"
mkdir_report "$TARGET/.ai/snapshots"
mkdir_report "$TARGET/.ai/human-actions"
mkdir_report "$TARGET/.ai/domain-candidates"
for dir in inbox processed extracted reviews manifests rejected runs; do
  mkdir_report "$TARGET/.ai/documents/$dir"
done

for template in requirement implementation-plan decision-record verification-report handoff knowledge-entry blind-spot-report requirement-analysis skill-selection implementation-summary test-evidence review-report traceability document-intelligence-report document-review-report; do
  copy_if_missing "$TEMPLATE_ROOT/.ai/templates/$template.md" "$TARGET/.ai/templates/$template.md"
done
copy_if_missing "$TEMPLATE_ROOT/.ai/templates/run-state.json" "$TARGET/.ai/templates/run-state.json"
copy_if_missing "$TEMPLATE_ROOT/.ai/templates/document-manifest.json" "$TARGET/.ai/templates/document-manifest.json"
copy_if_missing "$TEMPLATE_ROOT/.ai/templates/domain-candidate.md" "$TARGET/.ai/templates/domain-candidate.md"

for agent in requirement-analyst memory-retriever blind-spot-reviewer skill-selector planner implementer tester reviewer verifier memory-curator handoff-writer document-analyst document-reviewer; do
  copy_if_missing "$TEMPLATE_ROOT/.ai/agents/$agent.md" "$TARGET/.ai/agents/$agent.md"
done

copy_if_missing "$TEMPLATE_ROOT/.ai/knowledge/index.md" "$TARGET/.ai/knowledge/index.md"
copy_if_missing "$TEMPLATE_ROOT/.ai/decisions/index.md" "$TARGET/.ai/decisions/index.md"
copy_if_missing "$TEMPLATE_ROOT/.ai/documents/index.md" "$TARGET/.ai/documents/index.md"
copy_if_missing "$TEMPLATE_ROOT/.ai/documents/README.md" "$TARGET/.ai/documents/README.md"
copy_if_missing "$TEMPLATE_ROOT/.ai/domain-packs.yaml" "$TARGET/.ai/domain-packs.yaml"
copy_if_missing "$TEMPLATE_ROOT/.ai/project.json" "$TARGET/.ai/project.json"
copy_if_missing "$TEMPLATE_ROOT/.ai/ai-core.yaml" "$TARGET/.ai/ai-core.yaml"
copy_if_missing "$TEMPLATE_ROOT/.ai/knowledge/knowledge-capture-rule.md" "$TARGET/.ai/knowledge/knowledge-capture-rule.md"

copy_if_missing "$TEMPLATE_ROOT/AGENTS.md" "$TARGET/AGENTS.md"
copy_if_missing "$TEMPLATE_ROOT/docs/project-overview.md" "$TARGET/docs/project-overview.md"
copy_if_missing "$TEMPLATE_ROOT/docs/architecture.md" "$TARGET/docs/architecture.md"
copy_if_missing "$TEMPLATE_ROOT/docs/glossary.md" "$TARGET/docs/glossary.md"
copy_if_missing "$TEMPLATE_ROOT/docs/known-issues.md" "$TARGET/docs/known-issues.md"
copy_if_missing "$TEMPLATE_ROOT/docs/ai-project-workflow.md" "$TARGET/docs/ai-project-workflow.md"
copy_if_missing "$TEMPLATE_ROOT/docs/memory-rules.md" "$TARGET/docs/memory-rules.md"
copy_if_missing "$TEMPLATE_ROOT/docs/memory-rollback.md" "$TARGET/docs/memory-rollback.md"
copy_if_missing "$TEMPLATE_ROOT/docs/blind-spot-pass.md" "$TARGET/docs/blind-spot-pass.md"
copy_if_missing "$TEMPLATE_ROOT/docs/agent-harness.md" "$TARGET/docs/agent-harness.md"
copy_if_missing "$TEMPLATE_ROOT/docs/document-intelligence.md" "$TARGET/docs/document-intelligence.md"
copy_if_missing "$TEMPLATE_ROOT/docs/domain-packs.md" "$TARGET/docs/domain-packs.md"

mkdir_report "$TARGET/scripts"
for script in capture-knowledge.py capture-decision.py validate-memory.py retrieve-memory.py validate-blind-spots.py run-blind-spot-pass.py run_blind_spot_constants.py run-agent-workflow.py validate-agent-run.py memorylib.py documentlib.py ingest-document.py extract-document.py analyze-document-intelligence.py review-document-intelligence.py promote-document-intelligence.py search-document-intelligence.py document-run.py validate-document-intelligence.py domainlib.py activate-domain-pack.py validate-domain-pack.py recommend-domain-packs.py create-domain-candidate.py upgrade-domain-pack.py; do
  if [ -f "$TEMPLATE_ROOT/scripts/$script" ]; then
    copy_if_missing "$TEMPLATE_ROOT/scripts/$script" "$TARGET/scripts/$script"
  fi
done
mkdir_report "$TARGET/scripts/parsers"
for parser_file in __init__.py base.py text_parser.py markdown_parser.py html_parser.py json_parser.py csv_parser.py docx_parser.py pdf_parser.py; do
  copy_if_missing "$TEMPLATE_ROOT/scripts/parsers/$parser_file" "$TARGET/scripts/parsers/$parser_file"
done

find_skill_path() {
  name="$1"
  for base in "$SKILLS_ROOT/custom" "$SKILLS_ROOT/third-party" "$SKILLS_ROOT/project-specific" "$SKILLS_ROOT"; do
    if [ -n "$SKILLS_ROOT" ] && [ -d "$base/$name" ]; then
      printf '%s\n' "$base/$name"
      return 0
    fi
  done
  return 1
}

if [ "${#LINK_SKILLS[@]}" -gt 0 ]; then
  for skill in "${LINK_SKILLS[@]}"; do
    if [ -z "$SKILLS_ROOT" ]; then
      echo "WARN skill $skill not linked; skills root not supplied or discoverable"
      continue
    fi
    skill_path="$(find_skill_path "$skill" || true)"
    if [ -z "$skill_path" ]; then
      echo "WARN skill $skill not found under $SKILLS_ROOT"
      continue
    fi
    link_path="$TARGET/.agents/skills/$skill"
    if [ -e "$link_path" ] || [ -L "$link_path" ]; then
      echo "SKIPPED link $link_path"
    else
      ln -s "$skill_path" "$link_path"
      echo "LINKED skill $link_path -> $skill_path"
    fi
  done
fi

echo "DONE initialized $TARGET"
