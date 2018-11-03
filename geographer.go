package main

import (
	"encoding/csv"
	"io"
	"os"
	"reflect"
	"strconv"
	// "fmt"
	"time"

	"github.com/RyanCarrier/dijkstra"
	"github.com/sjsafranek/ligneous"
)

var (
	Logger = ligneous.NewLogger()
	graph = dijkstra.NewGraph()
)

//**********************************************************************//
// Move to goutils package
func OpenFile(file string) (io.Reader, error) {
	var reader io.Reader

	// check if file exists
	if _, err := os.Stat(file); os.IsNotExist(err) {
		return reader, err
	}

	// Load a TXT/CSV file.
	fileHandler, err := os.Open(file)
	if nil != err {
		return reader, err
	}

	return fileHandler, nil
}

type FieldMismatch struct {
	expected, found int
}

func (e *FieldMismatch) Error() string {
	return "CSV line fields mismatch. Expected " + strconv.Itoa(e.expected) + " found " + strconv.Itoa(e.found)
}

type UnsupportedType struct {
	Type string
}

func (e *UnsupportedType) Error() string {
	return "Unsupported type: " + e.Type
}

// https://play.golang.org/p/kwc32A5mJf
func UnmarshalCsvRow(reader *csv.Reader, v interface{}) error {
	record, err := reader.Read()
	if err != nil {
		return err
	}
	s := reflect.ValueOf(v).Elem()
	if s.NumField() != len(record) {
		return &FieldMismatch{s.NumField(), len(record)}
	}
	for i := 0; i < s.NumField(); i++ {
		// fmt.Println(i, record[i])
		f := s.Field(i)
		if "" == record[i] {
			// set to nil ??
			continue
		}
		switch f.Type().String() {
		case "string":
			f.SetString(record[i])
		case "int":
			ival, err := strconv.ParseInt(record[i], 10, 0)
			if err != nil {
				return err
			}
			f.SetInt(ival)
		case "float64":
			fval, err := strconv.ParseFloat(record[i], 64)
			if err != nil {
				return err
			}
			f.SetFloat(fval)
		default:
			return &UnsupportedType{f.Type().String()}
		}
	}
	return nil
}

//**********************************************************************//

type Node struct {
	Highway  string  `json:"highway"`
	Osmid    int     `json:"osmid"`
	Ref      string  `json:"ref"`
	X        float64 `json:"x"`
	Y        float64 `json:"y"`
	Geometry string  `json:"geometry"`
}

type Edge struct {
	Access   string  `json:"access"`
	Area     string  `json:"area"`
	Bridge   string  `json:"bridge"`
	Geometry string  `json:"geometry"`
	Highway  string  `json:"highway"`
	Junction string  `json:"junction"`
	Key      int     `json:"key"`
	Lanes    string  `json:"lanes"`
	Length   float64 `json:"length"`
	Maxspeed string  `json:"maxspeed"`
	Name     string  `json:"name"`
	Oneway   string  `json:"oneway"`
	Osmid    int     `json:"osmid"`
	Ref      string  `json:"ref"`
	Service  string  `json:"service"`
	Tunnel   string  `json:"tunnel"`
	U        int     `json:"u"`
	V        int     `json:"v"`
	Width    string  `json:"width"`
}

func getNodes(in_file string) {
	csv_data, err := OpenFile(in_file)
	reader := csv.NewReader(csv_data)

	// read first line
	record, err := reader.Read()
	if nil != err {
		panic(err)
	}
	Logger.Debug("headers", record)

	// read lines from csv file
	for {
		var node Node
		err := UnmarshalCsvRow(reader, &node)
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}

		Logger.Info(node)

		graph.AddVertex(node.Osmid)
	}
}

func getEdges(in_file string) {
	csv_data, err := OpenFile(in_file)
	reader := csv.NewReader(csv_data)

	// read first line
	record, err := reader.Read()
	if nil != err {
		panic(err)
	}
	Logger.Debug("headers", record)

	// read lines from csv file
	for {
		var edge Edge
		err := UnmarshalCsvRow(reader, &edge)
		if err == io.EOF {
			break
		}
		if err != nil {
			panic(err)
		}

		Logger.Info(edge)
		graph.AddArc(edge.U,edge.,1)
	}
}

func main() {
	start_time := time.Now()

	getNodes("New York.nodes")
	getEdges("New York.edges")

	Logger.Infof("runtime %v", time.Since(start_time))
}
