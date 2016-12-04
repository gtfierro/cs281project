package main

import (
	"encoding/csv"
	"fmt"
	"github.com/gtfierro/pundat/client"
	bw "gopkg.in/immesys/bw2bind.v5"
	"log"
	"os"
	"strconv"
)

func main() {
	bwclient := bw.ConnectOrExit("")
	bwclient.OverrideAutoChainTo(true)
	vk := bwclient.SetEntityFromEnvironOrExit()

	motes := []string{
		"0024",
		"003a",
		"003f",
		"0046",
		"004a",
		"0024",
		"0055",
		"0037",
		"004f",
		"0040",
		"002f",
	}
	uuids := []string{}
	pc := client.NewPundatClient(bwclient, vk, "ucberkeley")
	uuidQueryFormat := `select uuid where path like "%s" and _name = "air_temp";`
	for _, mote := range motes {
		query := fmt.Sprintf(uuidQueryFormat, mote)
		fmt.Println(query)
		md, _, _, err := pc.Query(query)
		if err != nil {
			log.Fatal(err)
		}
		uuid := md.Data[0].UUID
		uuids = append(uuids, uuid)
	}
	fmt.Println(uuids)

	tsQueryFormat := `select data in ("11/30/2016", "11/23/2016") where uuid = "%s";`
	// get data and save it to CSV named by the mote
	for idx, uuid := range uuids {
		rows := [][]string{}
		query := fmt.Sprintf(tsQueryFormat, uuid)
		fmt.Println(query)
		_, ts, _, err := pc.Query(query)
		if err != nil {
			log.Fatal(err)
		}
		for tid, timestamp := range ts.Data[0].Times {
			rows = append(rows, []string{strconv.FormatUint(timestamp, 10), strconv.FormatFloat(ts.Data[0].Values[tid], 'f', -1, 64)})
		}
		fmt.Printf("wrote %d rows for %s\n", len(rows), motes[idx])
		f, err := os.Create(fmt.Sprintf("%s.csv", motes[idx]))
		if err != nil {
			log.Fatal(err)
		}
		writer := csv.NewWriter(f)
		err = writer.WriteAll(rows)
		if err != nil {
			log.Fatal(err)
		}
	}
}
