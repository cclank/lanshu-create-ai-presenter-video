# Finished examples: the KV cache explainer in nine styles

Each folder is the performed 45 s KV cache film of one style — the reference every `STARTER.md` idiom comes from.
Only the authored files are committed (`index.html`, `tools/sfx.py`, `fonts.json`, project files); `lib/`, fonts, and
audio are generated. To open one, copy it out of the skill and build it:

```bash
X=<skill>/explainer; S=v3-notebook
cp -R "$X/examples/kv-cache/$S" ./kv-$S
bash "$X/tools/sync.sh" ./kv-$S $S kv-cache      # no narration audio is committed: a silent track is used
python3 "$X/tools/fonts.py" ./kv-$S
(cd ./kv-$S && python3 tools/sfx.py && npx --yes hyperframes@0.8.81 preview)
```

V3 and V8 build their sound from a page log first: `node lib/kit/events.mjs .` (V3) or
`node lib/kit/chalklog.mjs .` (V8) before `tools/sfx.py`. To hear the voice, build the story with
`tools/story.py` (MiniMax key, or `--audio` with your own recording) and sync again.
