import {PageHeading, Section, Wrapper, SubSection} from "./styled";
import basicScript from './basic_script.json'
import parameterizedScript from './parameterized_script.json'
import AceEditor from "react-ace";
import React from "react";

export default function UserGuide() {
  return (
    <Wrapper>
      <PageHeading>User Guide</PageHeading>
      <div>
        With this tool, you can create dynamic whatsapp surveys where you can define the flow of questions based on the
        responses, dynamically modify the messages, sign up the users for follow-ups, and do much more using custom
        functions. <br/><br/>
        How to use this guide? If you are using the tool for the first time, head on to the tutorial. This is a hands-on
        tutorial that will give you a feel of what this tool is all about.
        Otherwise, feel free to jump to relevant sections.
      </div>
      <ul>
        <li>
          <a href={'#tutorial'}>Tutorial</a>
          <ul>
            <li>
              <a href={'#tutorial-basic'}>Basic survey</a>
            </li>
            <li>
              <a href={'#tutorial-params'}>Adding parameters</a>
            </li>
            <li>
              <a href={'#tutorial-next-condition'}>Next state control</a>
            </li>
          </ul>
        </li>
      </ul>
      <Section id={'tutorial'}>
        <div style={{fontSize: '30px'}}>Tutorial</div>
        <SubSection id={'tutorial-basic'}>
          <div style={{fontSize: '20px'}}>Basic survey</div>
          <div>
            We'll start by creating a basic survey that asks for the user's name and sends a greeting message.
            Right click on <b>+ New Survey</b> on the left pane and open it in new tab. You'll see a form with some text
            boxes
            and a script editor. Let's understand what these text boxes mean:
            <br/><br/>
            <u>Survey name</u>: A unique name for the survey. This name should not already be present in the system. All
            surveys need to
            have a unique name. <i>Fill in a unique survey name</i>
            <br/><br/>
            <u>Instance name</u>: Instance is used to group together similar surveys. For example, a set of surveys
            meant to
            collect information from coffee planters in Colombia can have an instance name such as - 'Coffee planters'.
            <i> For now, fill in this text box with the value <b>test</b></i>
            <br/><br/>
            <u>Start message</u>: This is a unique message that the user sends to start the survey. <i>Fill in with a
            unique
            start message, something like <b>start &lt;survey name&gt; </b></i>
            <br/><br/>
            <u>Comments</u>: This is just a helpful description of the survey
            <br/><br/>
            <u>Script</u>: Here we define the survey's flow of messages in JSON format. You should see a sample JSON
            script.
            Before we go into the details, delete the sample script and paste the following:
            <br/> <br/>
            <AceEditor
              mode="json"
              theme="monokai"
              name="deployment"
              readOnly={true}
              value={JSON.stringify(basicScript, null, 4)}
              fontSize={14}
              height={'370px'}
              width={'525px'}
              showPrintMargin={true}
              showGutter={true}
              highlightActiveLine={true}
              setOptions={{
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
                enableSnippets: false,
                showLineNumbers: true,
                tabSize: 2,
                useWorker: false,
              }}
            />
            <br/>
            Now, click on the button below the script editor - <b>Create Survey</b>! If the <i>Survey name</i> and
            <i> Start message</i> were unique, this will take you to the survey list. You should see the survey that
            you created at the bottom. Before moving on, let's actually test this survey. Take out your phone and open
            Whatsapp. Add a new contact: +1 (646) 217-0881, name it whatever you like. Send the <u>Start message</u> of
            the
            survey that you created to this number.
            <br/>
            This should start the survey and you should get a reply - "Hi, what is your name?". Type a random name like
            "John Doe".
            After sending this, you should see the next 2 messages - "Hello there!", "Hope you are having a great day!"
            Voila!
            It's that easy to create a survey.
            <br/><br/>
            <b>Please note: </b> When you start a survey by sending its start message to the whatsapp number, the system
            creates an active survey session for you and all the messages you send are considered a response to the active
            survey. You cannot start another survey in between. The active survey session ends when you complete it or don't
            respond for more than 24hrs.
            In case you want to leave a survey in the middle, you can send the term <b><i>"#bye" </i></b> without the quotes.
            After the session ends, you can start any other survey or the same survey again by sending the respective
            start message.
            <br/>
            <br/>
            Before we dive into the structure of the script, it is recommended that you
            familiarize yourself with JSON syntax. This is a good resource: &nbsp;
            <a target={'_blank'} href={'https://www.digitalocean.com/community/tutorials/an-introduction-to-json'}>
              https://www.digitalocean.com/community/tutorials/an-introduction-to-json
            </a>
            <br/><br/>
            Let's understand the JSON script now. On the left pane, click on <b>Surveys</b>, find your survey and click
            on it.
            This will take you
            to the edit page. Except the name of the survey, you can edit anything. The JSON script is where you define
            the
            messages and the flow of the survey:
            <br/><br/>
            <ul>
              <li>
                <b>"restart_word"</b>: The value of this key is used by the user to restart the survey if the user is in
                between
                the survey. You can try it out. Send the <u>Start message</u> of the survey to the whatsapp number. When
                you get the
                reply - "Hi, what is your name?", send <i>restart</i> This would restart the survey and you'll see the
                first message again.
              </li>
              <li>
                <b>"survey"</b>: Holds the messages and the order in the form of states. The states are defined as
                key-value pairs.
                The entry point of the survey is defined by the key "start" and this is a mandatory state for every
                survey.
              </li>
              <li>
                <b>"start"</b>: The value of the state is another object with key value pairs:
                <ul>
                  <li>
                    <b>"type"</b>: The value of this key
                    specifies the type of response that we expect from the user. This can be of 3 types:
                    <ul>
                      <li>
                        "var": This is used when we expect a text response from the user. Like a name.
                      </li>
                      <li>
                        "text": This is only used in the last state of the survey where we don't expect any response
                        from
                        the user. We used this type in the "greet" state.
                      </li>
                      <li>
                        "mcq": This type is used when we give users multiple options and ask them to reply with the
                        option
                        number. We'll see an example for this in a while
                      </li>
                    </ul>
                  </li>
                  <li>
                    <b>"msgs"</b>: This is an array of messages to be sent to the user. The system sends these messages
                    in
                    order with a pause of 1-2 seconds between them.
                  </li>
                  <li>
                    <b>"next"</b>: Here we specify which state to move to next after the user has responded to the msgs
                    in
                    the current state. In the example, we move to the "greet" state. <i> Please note that except the
                    "start"
                    state, the other states can be named anything you wish. For example, you can change the state name
                    from
                    "greet" to "bye bye"</i>
                  </li>
                </ul>
              </li>
              <li>
                <b>"greet"</b>: This is the last state of this survey. Notice that the "type" is <i>text</i>, which
                means
                that we don't expect any response from the user.
              </li>
            </ul>
          </div>
        </SubSection>
        <SubSection id={'tutorial-params'}>
          <div style={{fontSize: '20px'}}>Adding parameters</div>
          <div>
            Parameters can make the messages dynamic. Let's start by modifying the survey that we created in the previous step.
            Copy the below script, go to the edit page of your survey and paste it in the script editor. Now click <b>Save changes</b>
            &nbsp; at the bottom of the page.
            <br/> <br/>
            <AceEditor
              mode="json"
              theme="monokai"
              name="deployment"
              readOnly={true}
              value={JSON.stringify(parameterizedScript, null, 4)}
              fontSize={14}
              height={'630px'}
              width={'625px'}
              showPrintMargin={true}
              showGutter={true}
              highlightActiveLine={true}
              setOptions={{
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
                enableSnippets: false,
                showLineNumbers: true,
                tabSize: 2,
                useWorker: false,
              }}
            />
            <br/>
            Try it out using whatsapp. The changes can be tested instantaneously after Saving changes. Send the start message
            and complete the survey. Notice that the final message will greet you with the name that you entered as well as
            today's day. This kind of dynamism is made possible with the concept of <i>'Parameters'</i>
            <br/>
            <br/>
            We have added 2 parameters here. In the "msgs" of the "greet" state, you'll see <b>%%name%%</b> and <b>%%day%%</b>. Anything
            between 2 % signs is considered a parameter which is dynamically substituted when a user is taking the survey.
            We need to specify some logic on how to figure out the values for these parameters. That logic is defined in the
            <b>"params"</b> object. You can see two key-value pairs corresponding to the two parameters that we used in the msgs:
            <ul>
              <li>
                <b>"name"</b>: The 'name' parameter has to be substituted with the response of the previous state ie. "start"
                where the user responded with their name. To do this we have a function "get_from_response" with args "start".
                This function gets the response of one of the previous states and the state name from which you need the
                response has to be specified in the "args". There are many other functions that can be used. Please look at
                the <a href={'#'}>functions reference</a> to see the available functions and their supported args.
              </li>
              <li>
                <b>"day"</b>: This parameter has to be substituted with the day on which the user is taking this survey. For this,
                we have a function called "get_current_date". This function accepts the date format as "args". Here, we have
                used "%A" which returns the week day. Instead of %A, you can pass any valid format
                (<a href={'https://strftime.org/'} target={'_blank'}>https://strftime.org/</a>). Change the args from <b>"%A"</b> to
                &nbsp;<b>"%m-%d-%Y"</b> and Save changes. Now, try the survey from your Whatsapp. You'll see that the last message
                greets you with the whole date.
              </li>
            </ul>

          </div>
        </SubSection>
        <SubSection id={'tutorial-next-condition'}>
          <div style={{fontSize: '20px'}}>Next state control</div>
          <div>
            There are use cases where you might want to decide the next state based on some condition. For instance, let's
            say we have a survey that collects information about the weather conditions during planting season. We wouldn't
            want to collect the weather info if the user is out of the planting season. To be more clear, let's say the
            planting season for a crop is May - July. If a farmer takes the survey during these months, we would want to
            ask them the average amount of rainfall. But, if a farmer starts the survey in the month of December, we are not
            really interested in the weather conditions. So, we'd skip that question and ask the farmer to take the survey
            during planting season.
            <br/><br/>
            Another interesting use case is when we want to move to a state based on the user's response in one of the previous
            states. As an example, let's say we have a survey that asks user their language preference, based on which we can
            move to the state that has messages in the selected language. Let's see how we can implement these two use cases.
            <br/><br/>
            Edit the survey that you created previously by replacing the script with the following:
            <br/> <br/>
            <AceEditor
              mode="json"
              theme="monokai"
              name="deployment"
              readOnly={true}
              value={JSON.stringify(parameterizedScript, null, 4)}
              fontSize={14}
              height={'630px'}
              width={'625px'}
              showPrintMargin={true}
              showGutter={true}
              highlightActiveLine={true}
              setOptions={{
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
                enableSnippets: false,
                showLineNumbers: true,
                tabSize: 2,
                useWorker: false,
              }}
            />
            <br/>
            Test it out.
          </div>
        </SubSection>
      </Section>
    </Wrapper>
  )
}