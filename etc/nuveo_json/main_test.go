package main

import (
    "fmt"
    "net/http"
    "net/http/httptest"
    "net/url"
    "os"
    "reflect"
    "strings"
    "testing"
)

//data for tests
//data pre processed to be converted into Item
var pre_item_data_tests = []struct {
   map_item map[string]interface{}
   output Item
   expect bool
}{
    {
        map[string]interface{}{
            "cidade": "Piraporinha do Nor Sudoeste",
            "idade": "50",
            "sexo": "m",
            "estado": "Líquido",
            "nome": "Um nome",
            "email": "um@email.com",
            "lugar": 60,
        },
        Item{
            "Um nome",
            "um@email.com",
            "m",
            50,
            map[string]interface{}{
                "Cidade": "Piraporinha do Nor Sudoeste",
                "Estado": "Líquido",
                "Lugar": 60,
            },
        },
        true,
    },
    {
        map[string]interface{}{
            "cidade": "Maritacas",
            "idade": 10,
            "sexo": "f",
            "estado": "Cansada",
            "nome": "Um outro nome",
            "email": "mais_um@email.com"},
        Item{
            "Um outro nome",
            "mais_um@email.com",
            "f",
            10,
            map[string]interface{}{
                "Cidade": "Maritacas",
                "Estado": "Cansada",
            },
        },
        true,
    },
    {
        map[string]interface{}{
            "cidade": "Maritacas",
            "idade": 10.0,
            "sexo": "f",
            "estado": "Cansada",
            "nome": "Um outro nome",
            "email": "mais_um@email.com"},
        Item{
            "Um outro nome",
            "mais_um@email.com",
            "f",
            10,
            map[string]interface{}{
                "Cidade": "Maritacas",
                "Estado": "Cansada",
            },
        },
        true,
    },
    {
        map[string]interface{}{
            "cidade": "Maritacas",
            "idade": nil,
            "sexo": "50",
            "estado": nil,
            "nome": "Um outro nome",
            "email": "mais_um@email.com"},
        Item{
            "Um outro nome",
            "mais_um@email.com",
            "50",
            0,
            map[string]interface{}{
                "Cidade": "Maritacas",
            },
        },
        true,
    },
    {
        map[string]interface{}{
            "cidade": "Maritacas",
            "nome": "Um outro nome",
            "email": "mais_um@email.com"},
        Item{
            "Um outro nome",
            "mais_um@email.com",
            "",
            0,
            map[string]interface{}{
                "Cidade": "Maritacas",
            },
        },
        true,
    },
    {
        map[string]interface{}{},
        Item{},
        true,
    },
}

//data for tests
//raw csv data to test csv reading methods
var raw_csv_tests = []struct {
   //map_item map[string]interface{}
   csv string
   output ItemPack
   expect bool
}{
    {
        `estado,idade,nome,cidade,sexo,email,lugar
Líquido,50,"Um nome","Piraporinha do Nor Sudoeste",m,um@email.com,60
Cansada,10,"Um outro nome",Maritacas,f,mais_um@email.com,Lá
`,
        ItemPack{
            []Item{
                {
                    "Um nome",
                    "um@email.com",
                    "m",
                    50,
                    map[string]interface{}{
                        "Cidade": "Piraporinha do Nor Sudoeste",
                        "Estado": "Líquido",
                        "Lugar": "60",
                    },
                },
                {
                    "Um outro nome",
                    "mais_um@email.com",
                    "f",
                    10,
                    map[string]interface{}{
                        "Cidade": "Maritacas",
                        "Estado": "Cansada",
                        "Lugar": "Lá",
                    },
                },
            },
        },
        true,
    },
    {
        `estado,idade,nome,cidade,sexo,email
50,50,50,50,50,50
,,,,,
`,
        ItemPack{
            []Item{
                {
                    "50",
                    "50",
                    "50",
                    50,
                    map[string]interface{}{
                        "Cidade": "50",
                        "Estado": "50",
                    },
                },
                {},
            },
        },
        true,
    },
    {
        `estado,idade,nome,cidade,sexo,email`,
        ItemPack{},
        true,
    },
}


//data for tests
//raw json data to test json reading methods
var raw_json_tests = []struct {
   json string
   output ItemPack
   expect bool
}{
    {
`{
"data": [
{
  "cidade": "Piraporinha do Nor Sudoeste",
  "email": "um@email.com",
  "estado": "Líquido",
  "idade": 50,
  "nome": "Um nome",
  "sexo": "m",
  "lugar": 60
},
{
  "cidade": "Maritacas",
  "email": "mais_um@email.com",
  "estado": "Cansada",
  "idade": 10,
  "nome": "Um outro nome",
  "sexo": "f",
  "lugar": "Lá"
}
]}
`,
        ItemPack{
            []Item{
                {
                    "Um nome",
                    "um@email.com",
                    "m",
                    50,
                    map[string]interface{}{
                        "Cidade": "Piraporinha do Nor Sudoeste",
                        "Estado": "Líquido",
                        "Lugar": 60.0,
                    },
                },
                {
                    "Um outro nome",
                    "mais_um@email.com",
                    "f",
                    10,
                    map[string]interface{}{
                        "Cidade": "Maritacas",
                        "Estado": "Cansada",
                        "Lugar": "Lá",
                    },
                },
            },
        },
        true,
    },
    {
        `{"data": []}`,
        ItemPack{[]Item{}}, true,
    },
}


//code gotten from https://github.com/keighl/mandrill/blob/master/mandrill_test.go
//checks if the values `a` and `b` are equal
//raises testing error if they are different
func expect(t *testing.T, a interface{}, b interface{}) {
    if a != b {
        t.Errorf("Expected %v (type %[1]T) - Got %v (type %[2]T)", b, a)
    }
}

//code gotten from https://github.com/keighl/mandrill/blob/master/mandrill_test.go
//checks if the values `a` and `b` are different
//raises testing error if they are equal
func refute(t *testing.T, a interface{}, b interface{}) {
    if a == b {
        t.Errorf("Did not expect %v (type %[1]T) - Got %v (type %[2]T)", b, a)
    }
}

func reportif(a interface{}, b interface{}) {
    if !reflect.DeepEqual(a, b) {
        fmt.Printf("%v\n", a)
        fmt.Printf("%v\n", b)
        fmt.Println()
    }
}

//extracts the `attr` value from Item as a string
//in case of not being an attribute of `Item`
//gets it from `Item.Outros`
func ExtractValue(item Item, attr string) string {
    var i string
    r_item := reflect.ValueOf(item)

    item_value := reflect.Indirect(r_item).FieldByName(strings.Title(attr))
    if !item_value.IsValid() {
        i = fmt.Sprintf("%s", item.Outros[strings.Title(attr)])
    } else {
        switch item_value.Kind() {
            case reflect.Int:
                i = fmt.Sprintf("%d", item_value.Interface())
            default:
                i = fmt.Sprintf("%s", item_value.Interface().(string))
        }
    }
    return i
}

//code gotten from https://github.com/keighl/mandrill/blob/master/mandrill_test.go
//it mocks an http server to get the http data to process
//and store in the struct Item
func testTools(code int, body string, header string) (*httptest.Server, *Client)  {
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Content-Type", header)
        w.WriteHeader(code)
        fmt.Fprintln(w, body)
    }))

    transport := &http.Transport{
        Proxy: func(req *http.Request) (*url.URL, error) {
            return url.Parse(server.URL)
        },
    }

    httpClient := &http.Client{Transport: transport}
    client := &Client{server.URL, httpClient}

    return server, client
}


//checks the method FromJSON against some kinds of input
//data perfectly filled, swapped data, blank data
func TestFromJSON(t *testing.T) {
    for _, test := range pre_item_data_tests {
        result := Item{}
        result.FromJSON(test.map_item)

        reportif(test.output, result)
        expect(t, reflect.DeepEqual(test.output, result), test.expect)
    }
}


//checks the method GetCSV against some kinds of input
//asserts if it's return is a correctly filled ItemPack
func TestGetCSV(t *testing.T) {
    for _, test := range raw_csv_tests {
        server, client := testTools(200, test.csv, "text/csv")
        defer server.Close()

        response, _ := client.HTTPClient.Get(client.URL)
        result := client.GetCSV(response)
        defer response.Body.Close()

        //check if they have the same length
        reportif(len(result.Items), len(test.output.Items))
        expect(t, reflect.DeepEqual(len(result.Items), len(test.output.Items)), test.expect)

        for index, item := range test.output.Items {
            reportif(result.Items[index], item)
            expect(t, reflect.DeepEqual(result.Items[index], item), test.expect)
        }
    }

}


//checks the method GetJSON against some kinds of input
//asserts if it's return is a correctly filled ItemPack
func TestGetJSON(t *testing.T) {
    for _, test := range raw_json_tests {
        server, client := testTools(200, test.json, "application/json")
        defer server.Close()

        response, _ := client.HTTPClient.Get(client.URL)
        result := client.GetJSON(response, "data")
        defer response.Body.Close()

        //check if they have the same length
        reportif(len(result.Items), len(test.output.Items))
        expect(t, reflect.DeepEqual(len(result.Items), len(test.output.Items)), test.expect)

        for index, item := range test.output.Items {
            reportif(result.Items[index], item)
            expect(t, reflect.DeepEqual(result.Items[index], item), test.expect)
        }
    }
}


//checks the method MakeItems against some kinds of input
//asserts if it's return is a correctly filled ItemPack
func TestMakeItems(t *testing.T) {
    //test the json requests
    for _, test := range raw_json_tests {
        server, client := testTools(200, test.json, "application/json")
        defer server.Close()

        result := client.MakeItems()

        //check if they have the same length
        reportif(len(result.Items), len(test.output.Items))
        expect(t, reflect.DeepEqual(len(result.Items), len(test.output.Items)), test.expect)

        for index, item := range test.output.Items {
            reportif(result.Items[index], item)
            expect(t, reflect.DeepEqual(result.Items[index], item), test.expect)
        }
    }

    //test the csv requests
    for _, test := range raw_csv_tests {
        server, client := testTools(200, test.csv, "text/csv")
        defer server.Close()

        result := client.MakeItems()

        //check if they have the same length
        reportif(len(result.Items), len(test.output.Items))
        expect(t, reflect.DeepEqual(len(result.Items), len(test.output.Items)), test.expect)

        for index, item := range test.output.Items {
            reportif(result.Items[index], item)
            expect(t, reflect.DeepEqual(result.Items[index], item), test.expect)
        }
    }

    //test a request getting an error message
    server, client := testTools(404, `Not Found`, "text/html")
    defer server.Close()
    result := client.MakeItems()

    reportif(ItemPack{}, result)
    expect(t, reflect.DeepEqual(ItemPack{}, result), true)
}

// just checks if a call here prints correctly the values of an item
func TestPrintItems(t *testing.T) {
    test := raw_json_tests[0]
    server, client := testTools(200, test.json, "application/json")
    defer server.Close()
    client.PrintItems()
    // Output:
    // {Um nome um@email.com m 50 map[Lugar:60 Cidade:Piraporinha do Nor Sudoeste Estado:Líquido]}
    // {Um outro nome mais_um@email.com f 10 map[Estado:Cansada Lugar:Lá Cidade:Maritacas]}


}

//checks the method main against some kinds of input
func Test_Main(t *testing.T) {
    main()
    // Output:
    // Usage: 
    // go run main.go <url_to_retrieve>

    oldArgs := os.Args
    defer func() { os.Args = oldArgs }()
    os.Args = []string{"main", "mock://testing"}
    main()
    // Output:
    // Get mock://testing: unsupported protocol scheme "mock"
}

