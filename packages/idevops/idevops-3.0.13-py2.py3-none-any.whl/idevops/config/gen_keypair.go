package main

import (
	"flag"
	"fmt"
	"os"

	"github.com/iost-official/go-iost/account"
	"github.com/iost-official/go-iost/common"
	"github.com/iost-official/go-iost/crypto"
)

const KEYPAIR_OF_MASTER string = "keypairs_master"
const KEYPAIR_OF_SLAVE string = "keypairs_slave"

func main() {
	var m, s int
	flag.IntVar(&m, "m", 7, "number of master")
	flag.IntVar(&s, "s", 3, "number of slave")
	flag.Parse()

	gen_keypairs(m, s)
}

func gen_keypairs(m, s int) {
	master, err := os.Create(KEYPAIR_OF_MASTER)
	if err != nil {
		panic(err)
	}
	defer master.Close()

	for i := 0; i < m; i++ {
		ac, _ := account.NewKeyPair(nil, crypto.Ed25519)
		master.WriteString(fmt.Sprintf("%s,%s\n", ac.ReadablePubkey(), common.Base58Encode(ac.Seckey)))
	}

	slave, err := os.Create(KEYPAIR_OF_SLAVE)
	if err != nil {
		panic(err)
	}
	defer slave.Close()

	for i := 0; i < s; i++ {
		ac, _ := account.NewKeyPair(nil, crypto.Ed25519)
		slave.WriteString(fmt.Sprintf("%s,%s\n", ac.ReadablePubkey(), common.Base58Encode(ac.Seckey)))
	}
}
