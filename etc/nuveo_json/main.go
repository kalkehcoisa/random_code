package main

import (
    "encoding/csv"
    "encoding/json"
    "fmt"
    "io"
    "io/ioutil"
    "net/http"
    "os"
    "reflect"
    "strconv"
    "strings"
)

//code gotten from https://github.com/keighl/mandrill/blob/master/mandrill_test.go
//httpclient wrapper to be able to do tests using a mock server 
type Client struct {
    URL string
    HTTPClient *http.Client
}

//struct to store the data parsed from the json/csv file
type Item struct {
    Nome string `json:"nome"`
    Email string `json:"email"`
    Sexo string `json:"sexo"`
    Idade int `json:"idade"`
    Outros map[string]interface{} `json:"outros"`
}

type ItemPack struct {
    Items []Item
}

//populates an `Item` using the key value pair from `map_item`
func (i *Item) FromJSON(map_item map[string]interface{}) {
    for key, value := range map_item {
        attr_name := strings.Title(key)
        if reflect.TypeOf(value) != nil && value != "" {
            switch attr_name {
                case "Email":
                    i.Email = value.(string)
                case "Idade":
                    switch reflect.ValueOf(value).Kind() {
                        case reflect.Int:
                            i.Idade = value.(int)
                        case reflect.Float64:
                            i.Idade = int(value.(float64))
                        default:
                            i.Idade, _ = strconv.Atoi(value.(string))
                    }
                case "Nome":
                    i.Nome = value.(string)
                case "Sexo":
                    i.Sexo = value.(string)
                default:
                    if i.Outros == nil {
                        i.Outros = make(map[string]interface{})
                    }
                    i.Outros[attr_name] = value
            }
        }
    }
}

//method to populate `Item` objects with data gotten from a csv
//the data is retrieved from the http `response` it receives.
//returns an `ItemPack` that contains the new `Item` objects
//PS: doesn't take http response code into account
func (c *Client) GetCSV(response *http.Response) ItemPack {
    body, _ := ioutil.ReadAll(response.Body)
    reader := csv.NewReader(strings.NewReader(string(body)))

    //read the column names
    record, _ := reader.Read()
    columns := make([]string, len(record))
    for index, value := range record {
        columns[index] = strings.Title(value)
    }

    pack := ItemPack{}
    pack.Items = make([]Item, 0)
    for {
        values, err := reader.Read()
        if err == io.EOF {
            break
        }

        map_item := map[string]interface{}{}
        for index, key := range columns {
            map_item[key] = values[index]
        }
        item := Item{}
        item.FromJSON(map_item)
        pack.Items = append(pack.Items, item)
    }

    return pack
}

//method to populate `Item` objects with data gotten from a json
//the data is retrieved from the http `response` it receives.
//returns an `ItemPack` that contains the new `Item` objects
//`json_container` is a string with the variable name in the json
//containing the data
//PS: doesn't take http response code into account
func (c *Client) GetJSON(response *http.Response, json_container string) ItemPack {
    var aux map[string][]interface{}
    json.NewDecoder(response.Body).Decode(&aux)

    pack := ItemPack{}
    pack.Items = make([]Item, len(aux[json_container]))
    for index, record := range aux[json_container] {
        item := Item{}
        item.FromJSON(record.(map[string]interface{}))
        pack.Items[index] = item
    }
    return pack
}

//method to populate `Item` objects with data gotten from a json or csv
//the data is retrieved using the `Client.URL` address
//returns an `ItemPack` that contains the new `Item` objects
func (c *Client) MakeItems() ItemPack {
    response, err := c.HTTPClient.Get(c.URL)
    if err != nil {
        //return empty data
        fmt.Println(err)
        return ItemPack{}
    } else {
        defer response.Body.Close()
        resp_type := response.Header.Get("Content-Type")
        if strings.Index(resp_type, "text/csv") > -1 {
            return c.GetCSV(response)
        } else if strings.Index(resp_type, "application/json") > -1 {
            return c.GetJSON(response, "data")
        } else {
            //return empty data
            return ItemPack{}
        }
    }
}


//retrieves data and print it to the stdout
func (c *Client) PrintItems() {
    items := c.MakeItems()
    for _, item := range items.Items {
        fmt.Printf("%v\n", item)
    }
}


func main() {
    args := os.Args
    if len(args) != 2 {
        fmt.Println("Usage: ")
        fmt.Println("go run main.go <url_to_retrieve>")
    } else {
        url := args[1]
        httpClient := &http.Client{}
        client := Client{url, httpClient}
        client.PrintItems()
    }
}