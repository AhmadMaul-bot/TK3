import json, sys


def hitung_need(alloc, mx):
    return [[mx[i][j] - alloc[i][j] for j in range(len(mx[i]))]
            for i in range(len(mx))]


def banker(alloc, mx, avail):
    n, m = len(alloc), len(avail)
    need = hitung_need(alloc, mx)
    work, done, seq, log = avail[:], [False] * n, [], []
    while len(seq) < n:
        for i in range(n):
            if not done[i] and all(need[i][j] <= work[j] for j in range(m)):
                log.append((f"P{i}", need[i][:], work[:]))
                work = [work[j] + alloc[i][j] for j in range(m)]
                done[i] = True
                seq.append(f"P{i}")
                break
        else:
            return need, seq, log, False
    return need, seq, log, True


def cetak(need, seq, log, safe):
    print("Need:")
    for i, r in enumerate(need):
        print(f"  P{i}: {r}")
    print("\nIterasi:")
    for k, (p, nd, w) in enumerate(log, 1):
        print(f"  {k}. {p}: Need={nd} <= Work={w} -> selesai, "
              "Work baru = Work + Allocation")
    if safe:
        print("\nHasil: SAFE, urutan aman: " + " -> ".join(seq))
    else:
        stuck = [f"P{i}" for i in range(len(need)) if f"P{i}" not in seq]
        print(f"\nHasil: UNSAFE, tidak ada urutan aman (proses terjebak: {stuck})")


def permintaan(d, p, req):
    alloc, mx, avail = d["allocation"], d["max"], d["available"]
    need = hitung_need(alloc, mx)
    m = len(avail)
    print(f"Permintaan P{p}: {req}")
    print(f"  Need P{p} = {need[p]}, Available = {avail}")
    if any(req[j] > need[p][j] for j in range(m)):
        print("  DITOLAK: melebihi Need (melebihi klaim maksimum)")
        return
    if any(req[j] > avail[j] for j in range(m)):
        print("  DITUNDA: melebihi Available (proses harus menunggu)")
        return
    a2 = [r[:] for r in alloc]
    v2 = avail[:]
    for j in range(m):
        v2[j] -= req[j]
        a2[p][j] += req[j]
    print(f"  Alokasi sementara -> Available = {v2}, "
          f"Allocation P{p} = {a2[p]}, Need P{p} = {hitung_need(a2, mx)[p]}")
    _, seq, _, safe = banker(a2, mx, v2)
    if safe:
        print("  Hasil: AMAN, permintaan DIBERIKAN, urutan aman: "
              + " -> ".join(seq))
    else:
        print("  Hasil: TIDAK AMAN, permintaan DITOLAK (proses menunggu)")


if __name__ == "__main__":
    args = sys.argv[1:]
    berkas = args[0] if args and not args[0].startswith("--") else "data.json"
    d = json.load(open(berkas))
    if "--req" in args:      # contoh: --req 4 3 3 0  (P4 meminta 3,3,0)
        k = args.index("--req")
        permintaan(d, int(args[k + 1]), [int(x) for x in args[k + 2:]])
    else:
        cetak(*banker(d["allocation"], d["max"], d["available"]))
