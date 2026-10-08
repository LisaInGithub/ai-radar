/* GitHub Pages：沒有 Claude 資料庫時，改讀 data/ 資料夾裡的每日快照 */
(function(){
  if(window.claude)return;
  const J=p=>fetch("data/"+p,{cache:"no-cache"}).then(r=>r.ok?r.json():null).catch(()=>null);
  const man=J("manifest.json");
  const snap=docs=>({docs:docs.filter(Boolean).map(d=>({id:d.__id,data:()=>d}))});
  const one=d=>d?{exists:true,data:()=>d}:{exists:false,data:()=>({})};
  const tag=(arr,ids)=>arr.map((d,i)=>d&&Object.assign(d,{__id:ids[i]}));
  const colls={
    digests:async lim=>{const m=await man;const ids=((m&&m.digests)||[]).slice().sort().reverse().slice(0,lim||30);return tag(await Promise.all(ids.map(i=>J("digests/"+i+".json"))),ids)},
    experts:async lim=>{const m=await man;const ids=((m&&m.experts)||[]).slice().sort().reverse().slice(0,lim||30);return tag(await Promise.all(ids.map(i=>J("experts/"+i+".json"))),ids)},
    predictions:async()=>{const a=(await J("predictions.json"))||[];return a.map(d=>Object.assign(d,{__id:d.id}))}
  };
  const docs={"calendar/upcoming":"calendar.json","settings/voice":"settings-voice.json","settings/experts":"settings-experts.json","experts_meta/pool":"pool.json"};
  const db={
    collection(name){let lim=null;const q={orderBy(){return q},limit(n){lim=n;return q},onSnapshot(ok,bad){(colls[name]?colls[name](lim):Promise.resolve([])).then(a=>ok(snap(a))).catch(e=>bad&&bad(e))}};return q},
    doc(path){return{onSnapshot(ok){(docs[path]?J(docs[path]):Promise.resolve(null)).then(d=>ok(one(d)))},update(){return Promise.reject(new Error("GitHub 版本為唯讀"))}}}
  };
  window.claude={use:async k=>k==="db"?db:null};
})();
